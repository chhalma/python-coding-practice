"""
Day 4 — Software engineering through "design-as-code" classes (common interview asks).
Fill in each method (replace `raise NotImplementedError`), then run the file:
each test prints PASS / FAIL / TODO / ERROR.
Practise: clean class structure, type hints, validation + custom exceptions, edge cases.
Say out loud: what data structure you chose and the complexity of each method.
"""
import heapq
import itertools
from collections import OrderedDict, deque


class InvalidRequestError(ValueError):
    """Raised when a method is called with invalid arguments."""


# 1. Rate limiter — sliding window with deque (~25 min)
# Allow at most `limit` requests per user in any `window_seconds` window.
# Timestamps are passed in (seconds, non-decreasing) so it's testable.
#   rl = RateLimiter(limit=2, window_seconds=10)
#   rl.allow("u1", 0) -> True;  rl.allow("u1", 5) -> True;  rl.allow("u1", 6) -> False  (2 already in last 10s)
#   rl.allow("u1", 10) -> True   # the request at t=0 has left the window (window is (t-10, t])
# Raise InvalidRequestError if limit or window_seconds <= 0.
class RateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        raise NotImplementedError

    def allow(self, user_id: str, now: int) -> bool:
        raise NotImplementedError


# 2. LRU cache — OrderedDict (~20 min)
# get(key) returns the value or -1; put(key, value) inserts/updates.
# When over capacity, evict the Least Recently Used key (get and put both count as "use").
#   c = LRUCache(2); c.put(1, "a"); c.put(2, "b"); c.get(1) -> "a"
#   c.put(3, "c")   # evicts 2 (least recently used), not 1
#   c.get(2) -> -1
# Raise InvalidRequestError if capacity <= 0.
class LRUCache:
    def __init__(self, capacity: int) -> None:
        raise NotImplementedError

    def get(self, key: int):
        raise NotImplementedError

    def put(self, key: int, value) -> None:
        raise NotImplementedError


# 3. Call-centre queue — priority queue with heapq (~25 min)
# add_call(caller_id, priority): lower number = more urgent (1 = urgent, 3 = normal).
# next_call() returns the caller_id of the most urgent call; ties -> whoever called FIRST.
# next_call() on an empty queue raises InvalidRequestError. __len__ returns calls waiting.
#   q = CallQueue(); q.add_call("c1", 3); q.add_call("c2", 1); q.add_call("c3", 1)
#   q.next_call() -> "c2"; q.next_call() -> "c3"; q.next_call() -> "c1"
class CallQueue:
    def __init__(self) -> None:
        raise NotImplementedError

    def add_call(self, caller_id: str, priority: int) -> None:
        raise NotImplementedError

    def next_call(self) -> str:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


# ---------------------------------------------------------------- tests
def _raises(fn, exc) -> bool:
    try:
        fn()
    except exc:
        return True
    return False


def _test_rate_limiter() -> bool:
    rl = RateLimiter(limit=2, window_seconds=10)
    ok = [rl.allow("u1", 0), rl.allow("u1", 5), rl.allow("u1", 6), rl.allow("u1", 10)]
    other_user = rl.allow("u2", 6)  # limits are per user
    return (
        ok == [True, True, False, True]
        and other_user is True
        and _raises(lambda: RateLimiter(0, 10), InvalidRequestError)
    )


def _test_lru_cache() -> bool:
    c = LRUCache(2)
    c.put(1, "a")
    c.put(2, "b")
    first = c.get(1)            # 1 is now most recently used
    c.put(3, "c")               # evicts 2
    c.put(1, "A")               # update existing key, no eviction
    return (
        first == "a"
        and c.get(2) == -1
        and c.get(1) == "A"
        and c.get(3) == "c"
        and _raises(lambda: LRUCache(0), InvalidRequestError)
    )


def _test_call_queue() -> bool:
    q = CallQueue()
    q.add_call("c1", 3)
    q.add_call("c2", 1)
    q.add_call("c3", 1)
    waiting = len(q)
    order = [q.next_call(), q.next_call(), q.next_call()]
    return (
        waiting == 3
        and order == ["c2", "c3", "c1"]
        and len(q) == 0
        and _raises(q.next_call, InvalidRequestError)
    )


if __name__ == "__main__":
    for name, test in [
        ("1 RateLimiter", _test_rate_limiter),
        ("2 LRUCache", _test_lru_cache),
        ("3 CallQueue", _test_call_queue),
    ]:
        try:
            print(f"{'PASS' if test() else 'FAIL'}  {name}")
        except NotImplementedError:
            print(f"TODO  {name}")
        except Exception as e:
            print(f"ERROR {name}: {type(e).__name__}: {e}")
