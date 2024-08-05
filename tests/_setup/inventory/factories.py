import factory
import pytest
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from factory import Faker as RawFaker, LazyAttribute
from faker import Faker
from fastapi_users.password import PasswordHelper

from applications.tasks.models import TaskModel
from applications.users.models import UserModel
from tests.conftest import AsyncSessionLocal

faker = Faker("en_US")


class CustomSQLAlchemyOptions(AsyncSQLAlchemyFactory):
    @classmethod
    async def create(cls, **kwargs):
        async with AsyncSessionLocal() as session:
            cls._meta.sqlalchemy_session = session
            return await super().create(**kwargs)


class UserModelFactory(CustomSQLAlchemyOptions):
    email = LazyAttribute(lambda a: f"{a.first_name}.{a.last_name}@test.com".lower())
    hashed_password = factory.Sequence(lambda n: PasswordHelper().password_hash.hash(f"test_user_{n}@test.com"))
    first_name = RawFaker("first_name")
    last_name = RawFaker("last_name")
    is_active = True
    is_superuser = False
    last_login = faker.date_time_this_year()
    date_joined = faker.date_time_this_year()

    class Meta:
        model = UserModel

@pytest.fixture(scope="function")
def user_factory() -> type[UserModelFactory]:
    return UserModelFactory


class TaskModelFactory(CustomSQLAlchemyOptions):
    url = factory.Faker("url")
    owner_id = factory.SubFactory(UserModelFactory)

    class Meta:
        model = TaskModel


@pytest.fixture(scope="function")
def task_factory() -> type[TaskModelFactory]:
    return TaskModelFactory
