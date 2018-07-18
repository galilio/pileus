from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import Future
from concurrent.futures import wait
from concurrent.futures import FIRST_EXCEPTION

class Async(object):
    def __init__(self, max_workers = None):
        self.fs = []
        self.executor = ThreadPoolExecutor(max_workers)
    
    def do(self, fn, *args, **kwargs):
        fut = self.executor.submit(fn, *args, **kwargs)
        self.fs.append(fut)
        return self
    
    def __del__(self):
        self.executor.shutdown(wait = False)

    def __call__(self, timeout = None):
        if not self.fs:
            return

        done, not_done = wait(self.fs, timeout = timeout, return_when = FIRST_EXCEPTION)
        for f in done:
            if not f.cancelled() and f.exception() is not None:
                if not_done:
                    for nf in not_done:
                        print('cancel running future')
                        nf.cancel()
                self.executor.shutdown(wait = False)
                raise f.exception()

        retval = [f.result(timeout = 0) for f in self.fs]
        self.executor.shutdown(wait = False)
        return retval

def async(max_workers = None):
    return Async(max_workers = max_workers)




