# shared_store.py
import threading
from typing import Dict, Any

class ThreadSafeDict:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()
    
    def get(self, key, default=None):
        with self._lock:
            return self._data.get(key, default)
    
    def __getitem__(self, key):
        with self._lock:
            return self._data[key]
    
    def __setitem__(self, key, value):
        with self._lock:
            self._data[key] = value
    
    def clear(self):
        with self._lock:
            self._data.clear()

url_time = ThreadSafeDict()
BASE64_STORE = ThreadSafeDict()
