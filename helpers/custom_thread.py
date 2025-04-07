from threading import Thread

class TomChienXuOJThread(Thread):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._return_data = None

  def run(self):
    if self._target is not None:
      self._return_data = self._target(*self._args, **self._kwargs)

  def join(self, *args, **kwargs):
    Thread.join(self, *args, **kwargs)
    return self._return_data