import time
from threading import Lock

# Thread-safe in-memory store
url_store = {}
click_stats = {}
store_lock = Lock()

def save_url_mapping(short_code, original_url):
    with store_lock:
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%S')
        url_store[short_code] = {
            "original_url": original_url,
            "created_at": timestamp,
            "clicks": 0
        }

def get_original_url(short_code):
    with store_lock:
        return url_store.get(short_code)

def increment_click(short_code):
    with store_lock:
        if short_code in url_store:
            url_store[short_code]["clicks"] += 1

def get_stats(short_code):
    with store_lock:
        return url_store.get(short_code)
