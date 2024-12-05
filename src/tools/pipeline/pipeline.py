import time
from collections.abc import Callable
from queue import PriorityQueue
from typing import Any

from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeRemainingColumn
from rich.table import Column
from tools.pipeline.custom_q import CustomQ
from tools.pipeline.worker import Worker


class Pipeline:
    __queue: CustomQ = None
    __priority_queue: PriorityQueue = None
    __max_workers: int = 10
    __func_processing: Callable[[Any], Any]
    __workers: list[Worker] = []

    def __init__(
        self,
        data: list[Any],
        func: Callable[[Any], Any],
        count_workers: int = 10,
        name: str = "Worker",
    ):
        self.__max_workers = count_workers
        self.__func_processing = func
        self.len_data = len(data)
        self.__name = name
        self.__queue = CustomQ.create(data)
        self.__priority_queue = PriorityQueue()
        self.__prepare_processes_bar()
        self.__create_job_progress()

    def __prepare_processes_bar(self):
        # {task.completed} of {task.total} | {task.percentage:>3.0f}% {task.elapsesd}
        text_column = TextColumn("{task.description} -> {task.completed} of {task.total}  ")
        bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
        task_column = TaskProgressColumn()
        time_column = TimeRemainingColumn()
        self.job_progress = Progress(text_column, time_column, bar_column, task_column, expand=True)
        self.__queue.task_id = self.job_progress.add_task(self.__name, total=self.len_data)
        self.job_progress.start()

    def __create_job_progress(self):
        for _ in range(self.__max_workers):
            worker = Worker(
                in_=self.__queue,
                out_=self.__priority_queue,
                func_processing=self.__func_processing,
                func_bar_increment=self._redraw_progress,
            )
            worker.start()
        self.__queue.queue.join()

    def _redraw_progress(self, job_id):
        self.job_progress.update(job_id, advance=1)
        time.sleep(0.12)

    @property
    def data(self):
        data = []
        while not self.__priority_queue.empty():
            data.append(self.__priority_queue.get())
        return data
