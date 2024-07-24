import logging
import sys
from concurrent import futures


class AsyncLogDispatcher(logging.Handler):
    """
    Определяет способ ведения асинхронного логирования.

    :param use_thread:  использование асинхронного режима, предоставляемого ThreadPoolExecutor.
    :param use_celery: доступен ли Celery.
    :param thread_worker: Максимальное количество рабочих ThreadPoolExecutor.
                          Если не задано, по умолчанию будет установлено количество процессоров на машине.
    """

    importer = staticmethod(__import__)

    def __init__(
        self,
        func,
        use_thread=True,
        use_celery=False,
        thread_worker=None,
        *args,
        **kwargs
    ):

        if use_thread and use_celery:
            raise ValueError("Can not both use thread and celery.")
        elif not use_thread and not use_celery:
            raise ValueError(
                "None of approach are given, set either use_thread or "
                "use_celery to True.",
            )

        if isinstance(func, str):
            func = self.resolve(func)
        if use_thread and not callable(func):
            raise ValueError(
                "func must be a callable function while use_thread is True.",
            )
        elif use_celery and not hasattr(func, "delay"):
            raise ValueError(
                "Makesure Celery is available while use_celery is True.",
            )

        if thread_worker and not isinstance(thread_worker, int):
            raise ValueError("Integer expected for thread_worker argument.")

        self.func = func
        self.use_thread = use_thread
        self.use_celery = use_celery
        if use_thread:
            self._thread_executor = futures.ThreadPoolExecutor(
                max_workers=thread_worker,
            )
        else:
            self._thread_executor = None
        super().__init__(*args, **kwargs)

    def resolve(self, s):
        name = s.split(".")
        used = name.pop(0)
        try:
            found = self.importer(used)
            for frag in name:
                used += "." + frag
                try:
                    found = getattr(found, frag)
                except AttributeError:
                    self.importer(used)
                    found = getattr(found, frag)
            return found
        except ImportError:
            e, tb = sys.exc_info()[1:]
            v = ValueError("Cannot resolve {!r}: {}".format(s, e))
            v.__cause__, v.__traceback__ = e, tb
            raise v

    def close(self):

        if self.use_thread and self._thread_executor:
            self._thread_executor.shutdown(wait=True)
        super().close()

    def emit(self, record):
        msg = self.format(record)
        if self.use_thread and self._thread_executor:
            self._thread_executor.submit(self.func, msg)
        elif self.use_celery:
            self.func.delay(msg)
