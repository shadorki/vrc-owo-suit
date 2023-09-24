class Event:
    def __init__(self):
        self.listeners = []

    def add_listener(self, func):
        self.listeners.append(func)

    def remove_listener(self, func):
        self.listeners.remove(func)

    def dispatch(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)