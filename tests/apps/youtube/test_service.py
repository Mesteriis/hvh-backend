import pytest
from kombu.transport.sqlalchemy import metadata

from applications.tasks.models import TaskModel
from applications.youtube.models import YTVideoModel
from applications.youtube.service import YTItemInteractor, YTItemSelector
from applications.youtube.structs import YTItemStruct

pytestmark = pytest.mark.unit


class TestYTItemSelector:
    service = YTItemSelector(YTVideoModel)

    async def test_get_by_id(self, user_factory, task_factory, yt_video_factory):
        user = await user_factory.create()
        task = await task_factory.create(owner_id=user.pk)
        video = await yt_video_factory.create(
            owner_id=user.pk,
            task_id=task.pk
        )
        video_in_db = await self.service.get_by_id(video.id)
        assert video_in_db.meta_data

    async def test_get_by_ext_id(self, user_factory, task_factory, yt_video_factory):
        user = await user_factory.create()
        task = await task_factory.create(owner_id=user.pk)
        video = await yt_video_factory.create(
            owner_id=user.pk,
            task_id=task.pk
        )
        video_in_db = await self.service.get_by_ext_id(video.ext_id)
        assert video_in_db.id == video.id
        assert video_in_db.owner_id == user.pk
        assert video_in_db.task_id == task.pk
        assert video_in_db.meta_data
        assert video_in_db.ext_id == video.ext_id

    async def test_get_all(self, user_factory, task_factory, yt_video_factory):
        user = await user_factory.create()
        task = await task_factory.create(owner_id=user.pk)
        await yt_video_factory.create_batch(
            5,
            owner_id=user.pk,
            task_id=task.pk
        )
        videos_in_db = await self.service.get_all()
        assert len(videos_in_db) >= 5

    async def test_get_by_owner(self, user_factory, task_factory, yt_video_factory):
        user = await user_factory.create()
        task = await task_factory.create(owner_id=user.pk)
        await yt_video_factory.create_batch(
            5,
            owner_id=user.pk,
            task_id=task.pk
        )
        videos_in_db = await self.service.get_by_owner(user.pk)
        assert len(videos_in_db) == 5

    async def test_get_by_status(self, user_factory, task_factory, yt_video_factory):
        user = await user_factory.create()
        task = await task_factory.create(owner_id=user.pk)

        await yt_video_factory.create_batch(
            5,
            owner_id=user.pk,
            task_id=task.pk
        )
        videos_in_db = await self.service.get_by_status("new")
        assert len(videos_in_db) >= 5


class TestYTItemInteractor:
    service = YTItemInteractor(YTVideoModel)

    async def test_create(self, user_factory, task_factory):
        user = await user_factory.create()
        task = await task_factory.create(owner_id=user.pk)
        data = YTItemStruct.model_validate(
            {
                "owner": user,
                "task": task,
                "meta_data": None,
                "status": "new",
                "ext_id": "1234"
            }
        )
        video = await self.service.create(data)
        assert video.owner.id == user.pk
        assert video.task.id == task.pk
