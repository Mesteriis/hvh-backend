import pytest

from applications.youtube.models import YTVideo
from applications.youtube.service import YTItemSelector

pytestmark = pytest.mark.unit


class TestSelector:
    service = YTItemSelector

    async def test_get_by_id(self, user_factory, task_factory, yt_video_factory):
        user = await user_factory.create()
        task = await task_factory.create(owner_id=user.pk)
        video = await yt_video_factory.create(
            owner_id=user.pk,
            task_id=task.pk
        )
        video_in_db = await self.service.get_by_id(YTVideo, video.id)
        assert video_in_db.id == video.id
        assert video_in_db.owner_id == user.pk
        assert video_in_db.task_id == task.pk
        assert video_in_db.meta_data

    def test_get_by_ext_id(self, selector, mocker):
        selector.__model.objects.get = mocker.CoroutineMock()
        selector.get_by_ext_id("test")
        selector.__model.objects.get.assert_called_once()

    def test_get_all(self, selector, mocker):
        selector.__model.objects.all = mocker.CoroutineMock()
        selector.get_all()
        selector.__model.objects.all.assert_called_once()
