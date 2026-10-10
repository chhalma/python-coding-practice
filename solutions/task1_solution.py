# Task 1 — Request log summary (reference solution)
#
# Clarifying questions → assumptions:
#   - Malformed line = not exactly 5 space-separated fields, or status/latency not integers.
#   - "Error" = status >= 500 only (404 is a client error, not counted).
#   - error_rate is a fraction 0..1; averages over all requests on that path; round to 2 dp.
#   - Output shape: {"paths": {path: {count, error_rate, avg_latency_ms}}, "skipped": int}
#
# Expected for LINES (worked by hand):
#   /api/jobs : 3 requests, 1 error (500)  → error_rate 0.33, avg (120+340+95)/3 = 185.0
#   /api/users: 1 request,  0 errors (404) → error_rate 0.0,  avg 30.0
#   skipped: 1 ("bad line here")

from collections import defaultdict
from dataclasses import dataclass

LINES = [
    "2026-10-06T10:00:01 GET /api/jobs 200 120",
    "2026-10-06T10:00:02 POST /api/jobs 500 340",
    "2026-10-06T10:00:03 GET /api/jobs 200 95",
    "bad line here",
    "2026-10-06T10:00:04 GET /api/users 404 30",
]


@dataclass
class PathStats:
    """Running totals for one path. Averages are computed at the end."""
    count: int = 0
    errors: int = 0
    total_latency: int = 0


def parse_line(line: str) -> tuple[str, int, int] | None:
    """Return (path, status, latency_ms), or None if the line is malformed."""
    parts = line.split()
    if len(parts) != 5:
        return None
    _timestamp, _method, path, status_str, latency_str = parts
    try:
        return path, int(status_str), int(latency_str)
    except ValueError:
        return None


def summarise(lines: list[str]) -> dict:
    stats: defaultdict[str, PathStats] = defaultdict(PathStats)
    skipped = 0

    # Pass 1: accumulate raw totals per path.
    for line in lines:
        parsed = parse_line(line)
        if parsed is None:
            skipped += 1
            continue
        path, status, latency = parsed

        s = stats[path]              # creates PathStats() on first sight of this path
        s.count += 1
        s.total_latency += latency
        if status >= 500:
            s.errors += 1

    # Pass 2: turn totals into the output shape.
    # count is always >= 1 here: a path only exists in stats once a line for it was counted.
    paths = {
        path: {
            "count": s.count,
            "error_rate": round(s.errors / s.count, 2),
            "avg_latency_ms": round(s.total_latency / s.count, 2),
        }
        for path, s in stats.items()
    }
    return {"paths": paths, "skipped": skipped}


# --- tests ---
result = summarise(LINES)
assert result["skipped"] == 1
assert result["paths"]["/api/jobs"] == {"count": 3, "error_rate": 0.33, "avg_latency_ms": 185.0}
assert result["paths"]["/api/users"] == {"count": 1, "error_rate": 0.0, "avg_latency_ms": 30.0}

assert summarise([]) == {"paths": {}, "skipped": 0}                         # empty input
assert summarise(["only bad"]) == {"paths": {}, "skipped": 1}               # all malformed
assert summarise(["t GET /x 200 abc"])["skipped"] == 1                      # 5 parts, bad latency

print(result)
print("all tests passed")

# Complexity: O(n) time over lines; O(p) space for p distinct paths.
# Improvements:
#   - Stream from a file with a generator so memory stays O(p) for huge logs.
#   - Log/collect skipped lines with line numbers (enumerate) instead of just counting.
#   - Validate status range (100–599) and non-negative latency; add p95 latency (needs per-path lists or a sketch).
