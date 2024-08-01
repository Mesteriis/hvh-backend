from apps.tasks.service import TaskSelector


class TestTaskSelector:

    def test_get_all(self, alembic_runner):
        assert TaskSelector.get_all(alembic_runner) == []

    def test_get_by_id(self):
        assert False


class TestTaskInteractor:

    def test_create(self):
        assert False

    def test_update(self):
        assert False

    def test_delete(self):
        assert False
