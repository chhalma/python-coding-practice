## Counter → the top 2 of ["a", "b", "a", "c", "b", "a"]
from collections import Counter
nums = ["a", "b", "a", "c", "b", "a"]
print(Counter(nums).most_common(2))

## defaultdict(list) → group ["bob", "ben", "amy"] by first letter
from collections import defaultdict
names = ["bob", "ben", "amy"]
group =  defaultdict(list[str])
for name in names:
    group[name[0]].append(name)
print(dict(group))

## sorted a list of dicts by amount desc, then name asc. Include a tie.
rows = [
    {"name":"bob", "amount": 250},
    {"name":"rob", "amount": 150},
    {"name":"bell", "amount": 450},
    {"name":"amy", "amount": 250},
]

sort_name = sorted(rows, key = lambda r: r["name"])
sort_amount = sorted(sort_name, key = lambda r: -r["amount"])

print(sort_amount)

## sorted a dict {"ACC1": 100, "ACC2": 250, "ACC3": 100} by value desc, then key asc

act = {"ACC1": 100, "ACC2": 250, "ACC3": 100}

sorted_act = sorted(act.items(), key = lambda kv : (-kv[1],kv[0]))
print(list(sorted_act))

## heapq.nlargest(2, rows, key=...) on the list of dicts

import heapq

windows = heapq.nlargest(2, rows, key =  lambda r: r["amount"])
heap =[]
for r in rows:
    heapq.heappush(heap,(r["amount"], r["name"]))

## deque(maxlen=3): append 1 to 5 and print list(...) each time


from collections import deque
window = deque(maxlen=3)
for i in range(1,6):
    window.append(i)
    print(list(window))

## dataclass Transaction(txn_id: str, amount: float, currency: str = "USD"), create one and print it


from dataclasses import dataclass

@dataclass
class Transction:
    txn_id: str
    amount: float
    currency: str = "USD"

t1 =  Transction('t1',39,"GBP")
print(t1)

## @An empty set, then add "t1" twice and print it

seen = set()
seen.add(10)
seen.add(10)
print(seen)
## dict(zip(names, amounts)), and enumerate(names, start=1)

names = ["bob", "amy", "sam"]
amounts = [250, 150, 300]
print({n:a for n,a in zip(names, amounts)})

print([f"{i}.{n}" for i,n in enumerate(names,start=1)])
"""
set maths: required = {"a", "b", "c"}, row = {"a": 1, "d": 2} → print the missing and the extra keys
"""
required ={"a", "b", "c"}
#required_set = set(required)
row = {"a": 1, "d": 2}
row_set =  set(row)
missing = required - row_set
extra = row_set - required
print(missing )
print(extra)