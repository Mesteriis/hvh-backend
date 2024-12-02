from queue import Queue
from typing import Self

from rich.progress import TaskID


class CustomQ:
    queue: Queue = None
    len_date: int = None
    data: list = None

    task_id: TaskID = None
    name: str = None

    @classmethod
    def create(cls, data, name: str = None) -> Self:
        queue_ = Queue()
        for item in data:
            queue_.put(item)
        q = cls()
        q.queue = queue_
        q.name = name or f'Task {id(q)}'
        q.len_date = len(data)
        q.data = data
        return q
