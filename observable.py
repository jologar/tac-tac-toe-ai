from typing import Callable
    
class Observable:
    def __init__(self):
        self._callbacks = []

    def subscribe(self, callback: Callable):
        if not callable(callback):
            raise TypeError("Callback parameter must be callable.")
        self._callbacks.append(callback)

    def unsuscribe(self, callback: Callable):
        self._callbacks.remove(callback)

    def fire(self):
        for callback in self._callbacks:
            callback()