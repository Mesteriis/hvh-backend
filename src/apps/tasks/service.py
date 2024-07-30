from apps.tasks.models import TaskModel


class TaskSelector:
    @classmethod
    def get_by_id(cls, task_id: int, db) -> TaskModel:
        return db.select(TaskModel).where(TaskModel.id == task_id).first()


class TaskInteractor:
    @classmethod
    def create(cls, task: TaskModel, db) -> TaskModel:
        return db.insert(task)

    @classmethod
    def update(cls, task: TaskModel, db) -> TaskModel:
        return db.update(task)

    @classmethod
    def delete(cls, task: TaskModel, db) -> TaskModel:
        return db.delete(task)
