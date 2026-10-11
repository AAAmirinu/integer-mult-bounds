"""Pure transcript-byte reuse; validation and hashing are never cached."""
from functools import lru_cache
import json
import pickle


class LineEncoder:
    def __init__(self, maxsize=262144):
        # Match json.dumps' defaults exactly. Reusing the encoder also avoids
        # constructing one encoder per event. Cache keys include all content.
        encoder = json.JSONEncoder(separators=(',', ':'))
        self._uncached = lambda value: (encoder.encode(value) + '\n').encode()
        self._enabled = bool(maxsize)
        # Pickle is only an internal, freshly computed key. It distinguishes
        # nested bool/int/float values that compare equal as Python tuples.
        # No external pickle is ever read; only our own dumps reach loads.
        self._cached = lru_cache(maxsize=maxsize)(
            lambda key: (encoder.encode(pickle.loads(key)) + '\n').encode())

    def line(self, value):
        if not self._enabled:
            return self._uncached(value)
        return self._cached(pickle.dumps(value, protocol=5))

    def statistics(self):
        return self._cached.cache_info()._asdict()


def integer_triple(value):
    a, b, c = value
    # This intentionally refuses bools, integer subclasses and non-integers.
    # Only the pinned scalar event call site supplies these three native ints.
    if not all(type(x) is int for x in (a, b, c)):
        raise TypeError('three native integer operands required')
    return ('[' + str(a) + ',' + str(b) + ',' + str(c) + ']').encode()
