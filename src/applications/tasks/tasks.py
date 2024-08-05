from celery import shared_task


@shared_task
def test_periodic_task():
    return 1 + 1
