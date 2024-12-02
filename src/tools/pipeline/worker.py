import queue
import threading
from logging import getLogger
from typing import Optional, Any, Callable

from icecream import ic

from tools.pipeline.custom_q import CustomQ

logger = getLogger(__name__)


class Worker(threading.Thread):
    all_elements = 0
    in_: CustomQ = None
    _func_processing: Callable = None
    _func_bar_increment: Callable = None

    def __init__(
            self,
            in_: CustomQ,
            out_: queue.PriorityQueue,
            func_processing: Callable,
            func_bar_increment: Callable
    ):
        super(Worker, self).__init__()
        self.setDaemon(True)

        self.in_ = in_
        self.out_ = out_
        self._func_processing = func_processing
        self._func_bar_increment = func_bar_increment

    def run(self):
        while True:
            job = self.in_.queue.get()
            try:
                data = self._func_processing(job)
                if type(data) is dict:
                    data = tuple(data.items())
                if data:
                    self.out_.put(data)
            except Exception as e:
                logger.error(f"In progress {job} error: {e}")
            self._func_bar_increment(self.in_.task_id)
            self.in_.queue.task_done()
