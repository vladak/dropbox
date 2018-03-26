import time
import contextlib


class Stopwatch():

    @staticmethod
    @contextlib.contextmanager
    def stopwatch(message):
        """Context manager to print how long a block of code took."""
        t0 = time.time()
        try:
            yield
        finally:
            t1 = time.time()
            print('Total elapsed time for %s: %.3f seconds' %
                  (message, t1 - t0))
