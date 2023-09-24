import atexit
from concurrent.futures import ThreadPoolExecutor


class Event:
    def __init__(self, max_workers=3):
        self.listeners = []
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        atexit.register(self.executor.shutdown)

    def add_listener(self, func):
        self.listeners.append(func)

    def remove_listener(self, func):
        self.listeners.remove(func)

    def dispatch(self, *args, **kwargs):
        for listener in self.listeners:
            self.executor.submit(listener, *args, **kwargs)
