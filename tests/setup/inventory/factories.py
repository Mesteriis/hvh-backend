import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from fastapi_users.password import PasswordHelper

from apps.tasks.models import TaskModel
from apps.users.models import UserModel
from tests.conftest import AsyncSessionLocal


class CustomSQLAlchemyOptions(AsyncSQLAlchemyFactory):
    @classmethod
    async def create(cls, **kwargs):
        async with AsyncSessionLocal() as session:
            cls._meta.sqlalchemy_session = session
            return await super().create(**kwargs)


class UserModelFactory(CustomSQLAlchemyOptions):
    email = factory.Sequence(lambda n: f"test_user_{n}@test.com")
    hashed_password = factory.Sequence(lambda n: PasswordHelper().password_hash.hash(f"test_user_{n}@test.com"))
    is_active = True
    is_superuser = False
    is_verified = True

    class Meta:
        model = UserModel


class TaskModelFactory(CustomSQLAlchemyOptions):
    url = factory.Faker("url")
    owner_id = factory.SubFactory(UserModelFactory)

    class Meta:
        model = TaskModel
