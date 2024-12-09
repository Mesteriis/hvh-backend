import pytest

from applications.tasks.models import TaskModel
from applications.youtube.models import YTVideoModel
from applications.youtube.service import YTItemSelector

pytestmark = pytest.mark.celery


async def test_parse_url_video(task_factory, user_factory, yt_url_video):
    user = await user_factory.create()
    task = await task_factory.create(
        url=yt_url_video,
        owner=user
    )
    # parse_url.apply((task.id,))
    task = await TaskModel.objects.get(pk=task.id)

    item = await YTItemSelector(YTVideoModel).get_by_task(task.id)
    assert item is not None

