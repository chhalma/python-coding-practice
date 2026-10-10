"""
1. Counter(...).most_common(2): the 2 most frequent words in a list
2. defaultdict(list): group ["alice", "bob", "anna", "ben", "carl"] by first letter
3. Sort a list of dicts by amount descending, then name ascending
4. heapq.nlargest(3, nums)
"""

from collections import Counter
words = ["buy", "sell", "go", "come", "buy","go","buy"]
print(Counter(words).most_common())

from collections import defaultdict
words =  ["alice", "bob", "anna", "ben", "carl"]
groups = defaultdict(list)
for w in words:
    groups[w[0]].append(w)
print(dict(groups))

rows = [
    {"name":"carl", "amount":50},
    {"name":"bob", "amount":150},
    {"name":"sam", "amount":40}
]
result =  sorted(rows, key=lambda r:(-r["amount"], r["name"]))
for r in result:
    print(r)

import heapq
nums = [3,1,5,7,2,9,4,3,7,2,99,44,5,44,99]
print(heapq.nlargest(3,nums))
print(heapq.nsmallest(3,nums))

"""
5. deque(maxlen=3): push 1 to 5 in turn and print the window after each push
6. @dataclass class Transaction with id: str, amount: float and currency: str = "USD"
"""

from collections import deque
window = deque(maxlen=3)

nums = [1,2,5,6,3,4]
for n in nums:
    window.append(n)
    print(list(window))

from dataclasses import dataclass

@dataclass
class Transaction:
    txn_id:str
    amount:float
    currency:str ="USD"

t1 = Transaction('t1', 12.4)
t2 = Transaction('t1', 12.4)
print(t1)
print(t1==t2)
"""
7. A dict comprehension, a set comprehension, enumerate, and zip
8. A parse_amount(s: str) -> float | None that uses try/except ValueError and is tested on "12.5" and "abc"
9. A generator function that yields lines one at a time (from a list or a file)
10. A custom exception class, raised and caught with a clear message
"""
pairs = {'a':100,'b':200,'c':300}
print({a:n for a,n in pairs.items() if n >150})

set_val = {1,2,3,4,5,3,2,5}
print({i for i in set_val})

names = ["alie","sam","bob","ziku"]
amounts = [20,13,28,33]
print({a:n  for a,n in zip(names,amounts) if n >15})

def parse_amount(s:str) ->float|None:
    try:
        return float(s)
    except ValueError:
        return None
print(parse_amount("12.5"))    # 12.5
print(parse_amount("abc"))     # None
print(parse_amount("0"))       # 0.0   ← must work
print(parse_amount(" 7 "))     # 7.0   ← float() strips whitespace



def read_lines(lines: list[str]):
    for line in lines:
        line = line.strip()
        if line:
            yield line

raw =  ["first\n","\n","second\n","\n","third\n"]
for line in read_lines(raw):
    print(line)

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
