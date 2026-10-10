"""
Refresh 4 — LeetCode patterns, one tool each.
Fill in each function body (replace `raise NotImplementedError`). Run the file:
each test prints PASS / FAIL / TODO. Aim: 3–8 lines per function, from memory.
Say out loud for each: the pattern, and the time/space complexity.
"""
import heapq
from collections import Counter, defaultdict, deque
from functools import lru_cache


# 1. Two Sum (LC 1) — dict "seen"
# Return indices [i, j] of the two numbers that add up to target.
#   two_sum([2, 7, 11, 15], 9) -> [0, 1]     # 2 + 7 = 9
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, n in enumerate(nums):
        complement =  target-n
        if complement not in seen:
            seen[n] =  i
        else:
            return [seen.get(complement),i]


# 2. Valid Parentheses (LC 20) — stack (plain list: append / pop)
# Every opener must be closed by the same type, in the right order.
#   is_valid("{[()]}") -> True
#   is_valid("([)]")   -> False      # wrong order
def is_valid(s: str) -> bool:
    pairs = {']':'[','}':'{', ')':'('}
    stack = []
    for c in s:
        if c in pairs:
            if not stack:
                return False
            b = pairs.get(c)
            top_b = stack.pop()
            if b != top_b:
                return False
        else:
            stack.append(c)
    return not stack

# 3. Group Anagrams (LC 49) — defaultdict(list), key = sorted letters
# Return the groups; order of groups doesn't matter.
# Anagrams = same letters, different order ("eat", "tea", "ate" all sort to "aet").
#   group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
#     -> [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
def group_anagrams(words: list[str]) -> list[list[str]]:
    groups = defaultdict(list)

    for w in words:
        key =  "".join(sorted(w))
        groups[key].append(w)
    return list(groups.values())


# 4. Top K Frequent Elements (LC 347) — Counter
# Return the k numbers that appear most often (any order).
#   top_k_frequent([1, 1, 1, 2, 2, 3], 2) -> [1, 2]     # 1 appears 3x, 2 appears 2x
import heapq
from collections import Counter
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    num_count = Counter(nums)
    return [n for n,c in num_count.most_common(k)] 
    ## or 
    ##print(heapq.nlargest(k,num_count,key=num_count.get))
    ##return list(heapq.nlargest(k,num_count,num_count.get))


# 5. Kth Largest Element (LC 215) — min-heap of size k with heappush / heappop
# Don't use sorted() or nlargest() here — practise the heap by hand.
#   kth_largest([3, 2, 1, 5, 6, 4], 2) -> 5     # sorted desc: 6, 5, ... → 2nd is 5
def kth_largest(nums: list[int], k: int) -> int:
    min_heap = []
    for n in nums:
        heapq.heappush(min_heap,n)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]
            

# 6. Shortest path in an unweighted graph — BFS with deque
# graph = {node: [neighbours]}. Return number of edges from start to goal, or -1.
#   graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": ["E"], "E": []}
#   shortest_path(graph, "A", "E") -> 3      # A→B→D→E (3 edges)
def shortest_path(graph: dict[str, list[str]], start: str, goal: str) -> int:
    queue =  deque([(start,0)])
    visited = {start}
    while queue:
        node, dist =  queue.popleft()
        if node == goal:
            return dist
        neighbours = graph[node]
        for n in neighbours:
            if n not in visited:
                visited.add(n)
                queue.append((n,dist+1))
                
            else:
                continue
    return  -1

# 7. Longest Substring Without Repeating Characters (LC 3) — sliding window + set
# Length of the longest CONTIGUOUS run with no repeated character.
#   longest_unique_substring("abcabcbb") -> 3    # "abc"
def longest_unique_substring(s: str) -> int:
    subStr = set()
    left = 0
    max_length = 0
    for i, c in enumerate(s):
        while c in subStr:
            subStr.remove(s[left])
            left += 1
        subStr.add(c)
        max_length = max(max_length, i-left+1)
    return max_length


# 8. Merge Intervals (LC 56) — sort by start, then merge
# Combine every set of overlapping [start, end] intervals.
#   merge_intervals([[1, 3], [2, 6], [8, 10]]) -> [[1, 6], [8, 10]]     # [1,3] and [2,6] overlap
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals = sorted(intervals)
    merge_irvl = [list(intervals[0])]
        
    for i in range(1,len(intervals)):
        intr =  intervals[i]
        s = intr[0]
        e = intr[1]
        le = merge_irvl[-1][1]
        if s <=  le:
            merge_irvl[-1][1] = max(e,le)
        else:
            merge_irvl.append(intr)
    return merge_irvl

# 9. Climbing Stairs (LC 70) — DP. You can climb 1 or 2 steps; how many ways to reach step n?
# Write it bottom-up (two variables). Bonus: a second version with @lru_cache recursion.
#   climb_stairs(3) -> 3    # 1+1+1, 1+2, 2+1
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    dp = [1]*n
    dp[0] = 1
    dp[1] = 2

    for i in range(2,n):
        dp[i] = dp[i-1] +dp[i-2]
    return dp[n-1]

# 10. Meeting Rooms II (LC 253) — sort by start + min-heap of end times
# Return the minimum number of rooms needed. Intervals are [start, end).
#   min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) -> 2     # [5,10] and [15,20] share room 2
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0
    intervals.sort()
    heap =[]
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap,end)
    return len(heap)


# ---------------------------------------------------------------- tests
def _tests() -> dict:
    return {
        "1 two_sum": lambda: (
            two_sum([2, 7, 11, 15], 9) == [0, 1]
            and two_sum([3, 3], 6) == [0, 1]
        ),
        "2 is_valid": lambda: (
            is_valid("()[]{}") and is_valid("{[()]}")
            and not is_valid("(]") and not is_valid("(") and not is_valid(")")
            and is_valid("")
        ),
        "3 group_anagrams": lambda: (
            sorted(sorted(g) for g in group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
            == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
            and group_anagrams([]) == []
        ),
        "4 top_k_frequent": lambda: (
            sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
            and top_k_frequent([7], 1) == [7]
        ),
        "5 kth_largest": lambda: (
            kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
            and kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
            and kth_largest([1], 1) == 1
        ),
        "6 shortest_path": lambda: (
            shortest_path({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": ["E"], "E": []}, "A", "E") == 3
            and shortest_path({"A": ["B"], "B": [], "C": []}, "A", "C") == -1
            and shortest_path({"A": []}, "A", "A") == 0
        ),
        "7 longest_unique_substring": lambda: (
            longest_unique_substring("abcabcbb") == 3
            and longest_unique_substring("bbbbb") == 1
            and longest_unique_substring("pwwkew") == 3
            and longest_unique_substring("") == 0
        ),
        "8 merge_intervals": lambda: (
            merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
            and merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
            and merge_intervals([[5, 6], [1, 2]]) == [[1, 2], [5, 6]]
            and merge_intervals([]) == []
        ),
        "9 climb_stairs": lambda: (
            climb_stairs(1) == 1 and climb_stairs(2) == 2
            and climb_stairs(3) == 3 and climb_stairs(5) == 8
        ),
        "10 min_meeting_rooms": lambda: (
            min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
            and min_meeting_rooms([[7, 10], [2, 4]]) == 1
            and min_meeting_rooms([[1, 5], [5, 10]]) == 1
            and min_meeting_rooms([]) == 0
        ),
    }


if __name__ == "__main__":
    for name, test in _tests().items():
        try:
            print(f"{'PASS' if test() else 'FAIL'}  {name}")
        except NotImplementedError:
            print(f"TODO  {name}")
        except Exception as e:  # show crashes without stopping the other tests
            print(f"ERROR {name}: {type(e).__name__}: {e}")
