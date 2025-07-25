import threading
from datetime import datetime

class URLStorage:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = {}  # { short_code: { "url": str, "clicks": int, "created_at": datetime } }

    def save_url(self, short_code, url):
        with self._lock:
            self._data[short_code] = {
                "url": url,
                "clicks": 0,
                "created_at": datetime.utcnow().isoformat()
            }

    def get_url(self, short_code):
        with self._lock:
            return self._data.get(short_code)

    def increment_click(self, short_code):
        with self._lock:
            if short_code in self._data:
                self._data[short_code]["clicks"] += 1

    def get_stats(self, short_code):
        with self._lock:
            return self._data.get(short_code)
