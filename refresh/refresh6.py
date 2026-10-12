import heapq
def kth_largest(nums: list[int], k: int) -> int:
    heap = []
    for n in nums:
        heapq.heappush(heap,n)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


## time: O(nlogn) as heapq is nlogn, space O(k)

def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    results = []
    intervals.sort()
    for start, end in intervals:
        if not results:
            results.append([start,end])
        else:
            l_end = results[-1][1]
            if start <= l_end:
                results[-1][1] = max(end, l_end)
            else:
                results.append([start,end])
    return results
## Time:O(n) space:O(n)

from collections import deque
def shortest_path(graph: dict[str, list[str]], start: str, goal: str) -> int: 
    if not graph:
        return -1
    queue = deque([(start,0)])
    visited = set()
    while queue:
        node, dis = queue.popleft()
        if node == goal:
            return dis
        neighbours =  graph[node]
        for n in neighbours:
            if n not in visited:
                queue.append((n,dis+1))
                visited.add(n)
            else: 
                continue
    return -1

## time: O(V+E) space: O(V)

def length_of_longest_substring(s: str) -> int: 
    seen = set()
    left = 0
    max_length = 0
    for i, c in enumerate(s):
        while c  in seen:
            seen.remove(s[left])
            left += 1
        seen.add(c)
        max_length = max(max_length, i-left+1)
    return max_length
## time: O(n) space: O(1) as alphabets are constant numbers

def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    dp = [1]*(n+1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n+1):
        dp[i] =  dp[i-1] +dp[i-2]
    return dp[n]
## time: O(n) space O(n)


def climb_stairs1(n: int) -> int:
    if n <= 2:
        return n
    prev2 = 1
    prev1 = 2
    for i in range(3, n+1):
        curr =  prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1

## time: O(n) space O(1)
import heapq
def min_meeting_rooms(intervals: list[list[int]]) -> int: 
    sorted_interval = sorted(intervals)
    heap = []
    for start,end in sorted_interval:
        if not heap:
            heapq.heappush(heap,end)
        else:
            if heap[0] <= start:
                heapq.heappop(heap)
                heapq.heappush(heap,end)
            else:
                heapq.heappush(heap, end)

    return len(heap)
## time:O(nlogn) space :O(n) in the worse case 

def merge_sorted(l1:list, l2:list)->list:
    result = []
    i=0#
    j = 0
    while (i<len(l1) and j<len(l2)):
        if l1[i] <= l2[j]:
            result.append(l1[i])
            i += 1
        else:
            result.append(l2[j])
            j += 1
    result.extend(l1[i:]) 
    result.extend(l2[j:])
    return result

## Time O(n+m) space O(n+m)

def max_profit(prices: list[int]) -> int:
    best_profit = float('-inf')
    min_price = float('inf')
    if not prices:
        return 0
    for p in prices:
        min_price = min(min_price, p)
        best_profit = max(best_profit, (p-min_price))
    return best_profit
## Time: O(n) space: O(1)

assert max_profit([7, 1, 5, 3, 6, 4]) == 5     # buy at 1, sell at 6
assert max_profit([7, 6, 4, 3, 1]) == 0        # prices only fall
assert max_profit([2, 4, 1]) == 2              # buy 2, sell 4 (the later "1" can't help)
assert max_profit([]) == 0

def first_bad(n: int, is_bad) -> int: 
    low = 1
    high = n
    while low < high:
        mid = (low+high)//2
        if is_bad(mid):
            high = mid
        else:
            low = mid+1

    return low

assert first_bad(5, lambda v: v >= 4) == 4
assert first_bad(1, lambda v: v >= 1) == 1
assert first_bad(100, lambda v: v >= 1) == 1
assert first_bad(100, lambda v: v >= 100) == 100
##  time: O(nlogn) space O(1)

def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    rows =  len(grid)
    cols = len(grid[0])
    island = 0
    def dfs(r,c):
        if r<0 or r>= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return False
    
        grid[r][c] = '0'
        dfs(r+1, c)
        dfs(r-1,c)
        dfs(r, c+1)
        dfs(r,c-1)
        return True
    for r in range(rows):
        for c in range(cols):
            if dfs(r,c):
                island += 1       
    return island     
 ## time : O(nm) space: O(1)


grid = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"],
]
assert num_islands(grid) == 3
assert num_islands([["0"]]) == 0
assert num_islands([["1", "1"], ["1", "1"]]) == 1
assert num_islands([]) == 0


from collections import defaultdict
def top_account(transactions: list[tuple[str, float]]) -> str | None:
    #res = defaultdict(str:float) = defaultdict(list)
    totals = defaultdict(float)
    for txn_id, amount in transactions:
        totals[txn_id] += amount
    if not totals:
        return None
    
    return min(totals.items(), key = lambda kv :(-kv[1],kv[0]))[0]

## time: O(n) space: ((nlogn))


if __name__ == "__main__":
        
    assert kth_largest([3,2,1,5,6,4], 2) == 5
    print("kth_largest passed")


    assert merge_intervals([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge_intervals([]) == []
    print("merge_intervals: all tests passed")

    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": ["E"], "E": []}
    assert shortest_path(graph, "A","E") == 3
    assert shortest_path(graph, "A","A") == 0
    assert shortest_path([], "A", "E") == -1
    assert shortest_path(graph, "A", "F") == -1
    
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("") == 0

    assert climb_stairs(5) == 8
    assert climb_stairs(0) == 0
    assert climb_stairs(2) == 2

    assert min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2

    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]