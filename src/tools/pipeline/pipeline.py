import math
import time
from queue import PriorityQueue
from typing import List, Dict, Any, Callable

from cffi.backend_ctypes import xrange
from icecream import ic

from tools.pipeline.custom_q import CustomQ

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn, TimeRemainingColumn
from rich.table import Table, Column

from tools.pipeline.worker import Worker


class Pipeline:
    __queue: CustomQ = None
    __priority_queue: PriorityQueue = None
    __max_workers: int = 10
    __func_processing: Callable[[Any], Any]
    __workers: List[Worker] = []

    def __init__(
            self,
            data: List[Any],
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
        text_column = TextColumn(
            "{task.description} -> {task.completed} of {task.total}  ")
        bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
        task_column = TaskProgressColumn()
        time_column = TimeRemainingColumn()
        self.job_progress = Progress(text_column,time_column, bar_column, task_column, expand=True)
        self.__queue.task_id = self.job_progress.add_task(self.__name, total=self.len_data)
        self.job_progress.start()
        # self.job_progress = Progress(
        #     "{task.description}",
        #     SpinnerColumn(),
        #     BarColumn(),
        #     TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        # )
        # for key, queue in self.__queues.items():
        #     queue.task_id = self.job_progress.add_task(f"[green] Tread #{key}", total=queue.len_date)
        # self.total = sum(task.total for task in self.job_progress.tasks)
        # overall_progress = Progress()
        # self.overall_task = overall_progress.add_task("All Jobs", total=int(self.total))
        #
        # progress_table = Table.grid()
        # progress_table.add_row(
        #     Panel.fit(
        #         overall_progress, title="Overall Progress", border_style="green", padding=(2, 2)
        #     ),
        #     Panel.fit(self.job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
        # )
        # self.live = Live(progress_table, refresh_per_second=24)

    def __create_job_progress(self):
        for _ in range(self.__max_workers):
            worker = Worker(
                in_=self.__queue,
                out_=self.__priority_queue,
                func_processing=self.__func_processing,
                func_bar_increment=self._redraw_progress
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
