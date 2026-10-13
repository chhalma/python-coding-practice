transactions = [
    {"customer": "A", "amount": 20, "status": "completed"},
    {"customer": "A", "amount": None, "status": "completed"},
    {"customer": "", "amount": 10, "status": "completed"},
    {"customer": "B", "amount": 7, "status": "FAILED"},
    {"customer": "B", "amount": 5, "status": "COMPLETED"},
    {"customer": "C", "amount": True, "status": "completed"},
]

"""
You are given a list of transaction records. Each transaction contains a customer ID, an amount and a status.
Write a Python function called summarise_transactions(transactions) that returns the total amount for each customer, counting only transactions with status "completed".

{"A": 35, "C": 30, "B": 5}
"""
from  collections import defaultdict
def summarise_transactions(transactions:list[dict])->dict:
    if not transactions:
        return {}
    summary = defaultdict(int)
    for t in transactions:
        customer = t["customer"] 
        amount = t["amount"]
        status =  t["status"]
        if status.lower() == "completed" and customer and isinstance(amount ,(int,float)) and not isinstance(amount,bool):
            summary[customer] += amount
    return dict(summary)
                        

assert summarise_transactions(transactions) == {"A": 20, "B": 5}
assert summarise_transactions([]) == {}
assert summarise_transactions([{"customer": "X", "amount": 9, "status": "failed"}]) == {}
assert summarise_transactions([{"status": "COMPLETED", "amount": 4, "customer": "Z"}]) == {"Z": 4}  # different key order + case

## Time:O(n) space :O(n) 

"""
Question 3 — First algorithmic problem
Interviewer:
Given a list of integers and a target value, return the indices of two different elements whose sum equals the target. Assume exactly one valid pair exists.
Example:nums = [2, 7, 11, 15]
target = 9
Expected output:[0, 1]
"""

def two_sum(nums:list[int], targert:int)-> list:
    seen =  {}
    for i,n in enumerate(nums):
        complement = targert -  n
        if complement in seen:
            return [seen[complement],i]
        seen[n]=i
    return []


assert two_sum([],10) == []
assert two_sum([3, 3], 6) == [0, 1]      # duplicates: must not reuse the same index
assert two_sum([3, 2, 4], 6) == [1, 2]   # the first element (3) is NOT part of the answer
assert two_sum([1, 2], 10) == []         # no solution
## Time: O(n), space:O(n)

"""
Question 4 — Strings and dictionaries
Interviewer:
Write a function called first_unique_char(s) that returns the index of the first character that appears exactly once in a string. If there is no such character, return -1.
Examples:
    first_unique_char("swiss")   # 1, character "w"
    first_unique_char("aabb")    # -1
    first_unique_char("leetcode") # 0, character "l"
    first_unique_char("")        # -1
"""
from collections import Counter

def first_unique_char(s)->int:
    char_count = Counter(s)
    for i, c in enumerate(s):
        if char_count[c] == 1:
            return i
    return -1
    
assert first_unique_char("swiss") == 1
assert first_unique_char("aabbcc") == -1
assert first_unique_char("") == -1

## time: O(nlogn) spcae:O(1)

"""
Given a string s, find the length of the longest substring that contains no repeated characters.
Examples:
    length_of_longest_substring("abcabcbb")  # 3
    length_of_longest_substring("bbbbb")     # 1
    length_of_longest_substring("pwwkew")    # 3
    length_of_longest_substring("")          # 0
"""

def length_of_longest_substring1(s: str) -> int:
    left = 0
    seen = set()
    largest_sub = 0
    for i,c in enumerate(s):
        while c in seen:
            seen.remove(s[left])
            left += 1
        seen.add(c)
        largest_sub = max(largest_sub, i-left+1 )
    return largest_sub

def length_of_longest_substring(s: str) -> int:
    max_count = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i,len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
            max_count = max(max_count,j-i+1)
    return max_count

assert length_of_longest_substring("abcabcbb") == 3
assert length_of_longest_substring("acn") == 3
assert length_of_longest_substring("") == 0
assert length_of_longest_substring("ababcdabcd") == 4

## Time:  O(n) space: O(1)