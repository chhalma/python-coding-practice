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
    count: int = 0
    errors: int = 0
    total_latency : int = 0

def parse_line(line:str)->tuple[str,int,int] | None:
    parts = line.split()
    if len(parts) != 5:
        return None
    _timestamp, _method, path, status_str, latency_str = parts
    try:
        return path, int(status_str) , int(latency_str)
    except ValueError:
        return None

def summarise(lines:list[str])->dict:
    skipped = 0
    result = defaultdict(PathStats)
    for line  in lines:
        parsed = parse_line(line)
        if parsed is None:
            skipped += 1
            continue
        path, status , latency = parsed

        r =  result[path]
        r.count +=1
        if status >= 500:
            r.errors += 1
        r.total_latency += latency
    paths = {
        path:{
            "count": r.count,
            "error_rate": round(r.errors/r.count,2),
            "avg_latency_ms": round(r.total_latency/r.count,2)

        } for path, r in result.items()

    } 
    return {"paths": paths ,"skipped": skipped}

"""
O(n) space: O(p) where p is distinct path
"""