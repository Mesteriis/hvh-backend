import factory
import pytest
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from factory import Faker as RawFaker, LazyAttribute
from faker import Faker

from applications.tasks.models import TaskModel
from applications.users.auth.utils.password import get_password_hash
from applications.users.models import UserModel
from applications.youtube.models import YTChannelModel, YTPlaylistModel, YTVideoModel
from tests.conftest import AsyncSessionLocal

faker = Faker("en_US")

from asyncio import run
class CustomSQLAlchemyOptions(AsyncSQLAlchemyFactory):
    @classmethod
    async def create(cls, **kwargs):
        async with AsyncSessionLocal() as session:
            cls._meta.sqlalchemy_session = session
            return await super().create(**kwargs)


# class UserModelFactory(CustomSQLAlchemyOptions):
class UserModelFactory(AsyncSQLAlchemyFactory):
    email = LazyAttribute(lambda a: f"{a.first_name}.{a.last_name}@test.com".lower())
    hashed_password = factory.Sequence(lambda n: get_password_hash(f"test_user_{n}@test.com"))
    first_name = RawFaker("first_name")
    last_name = RawFaker("last_name")
    is_active = True
    is_superuser = False
    last_login = faker.date_time_this_year()
    date_joined = faker.date_time_this_year()

    class Meta:
        model = UserModel
        # sqlalchemy_session_factory = AsyncSessionLocal
        sqlalchemy_session = AsyncSessionLocal()

@pytest.fixture(scope="function")
def user_factory() -> type[UserModelFactory]:
    return UserModelFactory


class TaskModelFactory(CustomSQLAlchemyOptions):
    url = factory.Faker("url")
    # owner_id = factory.LazyAttribute( lambda o: run(UserModelFactory.create()).id)
    owner_id = factory.SubFactory(UserModelFactory)

    class Meta:
        model = TaskModel


@pytest.fixture(scope="function")
def task_factory() -> type[TaskModelFactory]:
    return TaskModelFactory


class YTChannelFactory(CustomSQLAlchemyOptions):
    ext_id = factory.Faker("uuid4")
    owner_id = factory.SubFactory(UserModelFactory)
    task_id = factory.SubFactory(TaskModelFactory)

    meta_data = factory.LazyAttribute(
        lambda o: {
            "title": faker.sentence(),
            "description": faker.paragraph(),
            "thumbnail": faker.image_url(),
            "channel_id": faker.uuid4(),
            "playlist_id": faker.uuid4(),
            "tags": [faker.word() for _ in range(5)],
            "category_id": faker.uuid4(),
            "view_count": faker.random_int(),
            "like_count": faker.random_int(),
            "dislike_count": faker.random_int(),
            "comment_count": faker.random_int(),
        }
    )

    class Meta:
        model = YTChannelModel


@pytest.fixture(scope="function")
def yt_channel_factory() -> type[YTChannelFactory]:
    return YTChannelFactory


class YTPlaylistFactory(CustomSQLAlchemyOptions):
    ext_id = factory.Faker("uuid4")
    owner_id = factory.SubFactory(UserModelFactory)
    task_id = factory.SubFactory(TaskModelFactory)

    meta_data = factory.LazyAttribute(
        lambda o: {
            "title": faker.sentence(),
            "description": faker.paragraph(),
            "thumbnail": faker.image_url(),
            "channel_id": faker.uuid4(),
            "playlist_id": faker.uuid4(),
            "tags": [faker.word() for _ in range(5)],
            "category_id": faker.uuid4(),
            "view_count": faker.random_int(),
            "like_count": faker.random_int(),
            "dislike_count": faker.random_int(),
            "comment_count": faker.random_int(),
        }
    )

    class Meta:
        model = YTPlaylistModel


@pytest.fixture(scope="function")
def yt_playlist_factory() -> type[YTPlaylistFactory]:
    return YTPlaylistFactory


class YTVideoFactory(CustomSQLAlchemyOptions):
    ext_id = factory.Faker("uuid4")
    owner_id = factory.SubFactory(UserModelFactory)
    task_id = factory.SubFactory(TaskModelFactory)

    meta_data = factory.LazyAttribute(
        lambda o: {
            "title": faker.sentence(),
            "description": faker.paragraph(),
            "thumbnail": faker.image_url(),
            "channel_id": faker.uuid4(),
            "playlist_id": faker.uuid4(),
            "tags": [faker.word() for _ in range(5)],
            "category_id": faker.uuid4(),
            "view_count": faker.random_int(),
            "like_count": faker.random_int(),
            "dislike_count": faker.random_int(),
            "comment_count": faker.random_int(),
        }
    )

    class Meta:
        model = YTVideoModel


@pytest.fixture(scope="function")
def yt_video_factory() -> type[YTVideoFactory]:
    return YTVideoFactory
