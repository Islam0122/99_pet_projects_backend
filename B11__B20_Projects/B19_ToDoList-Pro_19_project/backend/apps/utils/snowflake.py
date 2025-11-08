import os
import time
import threading

NODE_ID = int(os.getenv("SNOWFLAKE_NODE_ID", "1")) & 0x3FF

_lock = threading.Lock()
_last_ts = 0
_sequence = 0

def _timestamp_ms():
    return int(time.time() * 1000)

def next_id():
    global _last_ts, _sequence
    with _lock:
        ts = _timestamp_ms()
        if ts == _last_ts:
            _sequence = (_sequence + 1) & 0xFFF
            if _sequence == 0:
                while ts <= _last_ts:
                    ts = _timestamp_ms()
        else:
            _sequence = 0
            _last_ts = ts
        id_ = (ts << (10 + 12)) | (NODE_ID << 12) | _sequence
        return id_
