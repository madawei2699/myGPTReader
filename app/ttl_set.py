from threading import Thread, Lock
import time

class TtlSet:
    def __init__(self):
        self.ttl = {}
        self.lock = Lock()
        # Start a background thread to periodically remove expired items
        t = Thread(target=self._cleaner)
        t.daemon = True
        t.start()

    def __len__(self):
        return len(self.ttl)

    def __contains__(self, value):
        return value in self.ttl

    def add(self, value, ttl_seconds):
        with self.lock:
            self.ttl[value] = time.time() + ttl_seconds

    def discard(self, value):
        with self.lock:
            self.ttl.pop(value, None)

    def _cleaner(self):
        while True:
            with self.lock:
                now = time.time()
                for k, v in list(self.ttl.items()):
                    if v < now:
                        self.ttl.pop(k, None)
            time.sleep(1)
