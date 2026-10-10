# Counter top 2 words
from collections import Counter

names = ["bel", "jel", "bella", "sam","bel"]
print(Counter(names).most_common(2))

nums = [2,1,3,4,2,3,4,5,6,7,3,4,5]
print(Counter(nums).most_common(3))

## defaultdict(list) grouping names by first letter
from collections import defaultdict

group_name =  defaultdict(list[str])
for n in names:
    group_name[n[0]].append(n)
print(dict(group_name))

# Sort dicts by amount descending, then name ascending

values = [{"name":"bella","amount":250},
{"name":"jilla","amount":150},
{"name":"dex","amount":350},
{"name":"sam","amount":50}
]
sorted_dict = sorted(values,key = lambda r:(-r["amount"], r["name"]))
print((sorted_dict))

## heapq.nlargest(3, ...)

import heapq

print(heapq.nlargest(3,nums)) #guessed

## deque(maxlen=3) window

from collections import deque

window = deque(maxlen=3)
for n in nums:
    window.append(n)
    print(window)

#print(window)


## @dataclass Transaction(txn_id, amount, currency="USD")

from dataclasses import dataclass 

@dataclass
class Transaction:
    txn_id:str
    amount:float=0.0
    currency:str="USD"

## One dict comprehension with a filter, one set comprehension, enumerate(start=1), dict(zip(...))

prices = {"bella": 250, "jilla": 150, "dex": 350, "sam": 50}
print({n:v for n,v in prices.items() if v> 200})

print({r["name"]:r["amount"] for r in values if r["amount"] > 200})
print({n for n in nums})
names = ["bob", "ami","sam"]
money = [23,12,45]
print([f"{i}.{name}" for i, name in enumerate(names,start =1 )])
print([(n,m )for n,m in zip(names,money)])


##  parse_amount returning float | None

def parse_amount(amount:str) ->float | None:
    try:
        return float(amount)
    except ValueError:
        return None

assert parse_amount("23.5") == 23.5
assert parse_amount("bob") is None

## A generator that yields non-blank stripped lines 

RAW_LINES = [
    "  2026-10-08 GET /api/jobs 200  \n",
    "\n",
    "   \n",
    "2026-10-08 POST /api/jobs 500\n",
    "# this is a comment\n",
    "2026-10-08 GET /api/users 404\n",
    "",
]
from collections.abc import Iterator
def generator(lines:list[str])->Iterator[str]:
    for line in lines:
        clean_line = line.strip()
        if clean_line:
            yield clean_line

        
result = generator(RAW_LINES)
print(next(result))

"""
A custom exception, raised and caught
"""

class InvalidTransactionError(ValueError):
    """Raised when a transaction fails validation."""


def validate_amount(amount: float) -> None:
    if amount < 0:
        raise InvalidTransactionError(f"Amount must be non-negative, got {amount}")


try:
    validate_amount(-5)
except InvalidTransactionError as e:
    print(f"Rejected: {e}")
# Rejected: Amount must be non-negative, got -5
