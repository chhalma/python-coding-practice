# python-coding-practice

Python coding practice: data structures & algorithms, data-processing tasks, and small system-design classes, with tests.

| Folder | What |
|---|---|
| `refresh/` | Python syntax drills and LeetCode-pattern problems (hash map, stack, heap, BFS, sliding window, intervals, DP) with a built-in PASS/FAIL runner |
| `tasks/` | Timed practical problems: log summary, transaction validation + dedup + aggregation |
| `solutions/` | Reference solutions for the tasks |
| `test/` | pytest tests |

## Run

```bash
python refresh/refresh4.py      # prints PASS / FAIL / TODO per problem
python -m pytest -q             # run the test suite
```

Requires Python 3.10+ and `pytest`.
