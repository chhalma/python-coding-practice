"""
Product of Array Except Self
Target: 10 minutes · Medium
Given a list of integers nums, return a list where each element is the product of all the other elements. Do not use division.
Example: [1, 2, 3, 4] → [24, 12, 8, 6]
"""

def product_of_array_except_self(nums:list[int])->list[int]:
    left = [1]*(len(nums))
    right = [1]*(len(nums))

    for i in range(1,len(nums)):
        left[i] = left[i-1]*nums[i-1]
        
    for j in range(len(nums)-2,-1,-1):
        right[j] = right[j+1]*nums[j+1]
        
    result = [left[i]*right[i] for i in range(len(nums))]
       
    return result
## Time: O(n) soace:O(n)
assert product_of_array_except_self([1,2,3,4]) == [24,12,8,6]

"""
Maximum Subarray
Target: 8–10 minutes · Medium
Find the largest sum of any non-empty contiguous subarray.
Example: [-2, 1, -3, 4, -1, 2, 1, -5, 4] → 6
"""

def largest_sum(nums:list[int])->int:
    best =  current = nums[0]
    for n in nums:
        current = max(n, current+n)
        best = max(best, current)
    return best

"""
Valid Anagram
Target: 5 minutes · Easy
Return True if strings s and t contain exactly the same characters with the same frequencies; otherwise return False.
Example: s = "listen", t = "silent" → True
"""
from collections import Counter
def anagram(s:str, t:str)-> bool:
    if len(s) != len(t):
        return False
    frq_s  = Counter(s)
    frq_t = Counter(t)

    for k,v in frq_s.items():
        if frq_t[k] == v:
            continue
        else:
            return False
    return True

assert anagram("listen", "silent") is True
assert anagram("aab", "abb") is False
assert anagram("", "") is True
assert anagram("a", "ab") is False

"""
nums = [0, 1, 0, 3, 12]
move_zeroes(nums)
assert nums == [1, 3, 12, 0, 0]

nums = [0, 0]
move_zeroes(nums)
assert nums == [0, 0]

nums = [1, 2, 3]
move_zeroes(nums)
assert nums == [1, 2, 3]
"""

def move_zero(nums:list[int])->list[int]:
    write = 0
    for  n in nums:
        if n != 0:
            nums[write] = n
            write += 1
    for i in range(write, len(nums)):
        nums[i] = 0
    return nums