"""
Merge Intervals
Target: 8 minutes · Medium
Merge all overlapping intervals and return the merged intervals in sorted order.
Example: [[1,3], [2,6], [8,10], [15,18]] → [[1,6], [8,10], [15,18]]
"""
def merge_interval(intervals:list[list[int]])->list[list[int]]:
    intervals.sort()
    results = []
    for interval in intervals:
        start, end = interval
        if results and start <= results[-1][1]:
            results[-1][1] =  max(results[-1][1], end)
        else:
            results.append(interval)
    return results

assert merge_interval([[1,3], [2,6], [8,10], [15,18]] ) == [[1,6], [8,10], [15,18]]
        

"""

1. Jump Game — Greedy
Problem: Given an array nums, where each element represents the maximum number of steps you can jump forward, determine whether you can reach the last index.
Example:nums = [2, 3, 1, 1, 4]
# Output: True
nums = [3, 2, 1, 0, 4]
# Output: False

"""
def jump_game(nums:list[int]) -> bool:
    farthest = 0
    for i , s in enumerate(nums):
        if i < farthest:
            return False
        farthest =  max(farthest,i+s)
    return True
"""
Minimum Number of Arrows to Burst Balloons — Greedy + Intervals
Problem: Each balloon is represented by an interval [start, end]. An arrow shot at position x bursts every balloon whose interval contains x. Find the minimum number of arrows needed to burst all balloons.
Example:
"""
def min_arrows(points:list[list[int]])->int:
    s_points = sorted(points,  key = lambda p:p[1])
    arrow = 0
    arrow_pos = float('-inf')
    for s, e in s_points:
       if s > arrow_pos:
           arrow += 1
           arrow_pos = e
    return arrow

assert min_arrows([[10, 16], [2, 8], [1, 6], [7, 12]])==2
"""
A network has n computers (nodes 0 to n-1) and a list of links (undirected edges). Some computers are compromised. You can't see which ones in advance, but you can call is_hacked(node) -> bool to check a computer.

A message must go from start to end, and it can only pass through computers that are not hacked (including start and end).

Return True if such a path exists, otherwise False.
"""
from collections import deque,defaultdict
def path_exists(n:int, computers:list[list[int]],start:int, end:int, is_hacked)->bool:
    if is_hacked(start) or is_hacked(end):
        return False
    queue =  deque([start])
    visited = {start}
    graph = defaultdict(list)
    for a,b in computers:
        graph[a].append(b)
        graph[b].append(a)
    while queue:
        node = queue.popleft()
        if node == end:
            return True
        neighbours = graph[node]
        for nb in neighbours:
            if not is_hacked(nb) and nb not in visited:
                visited.add(nb)
                queue.append(nb)

    return False

links = [[0, 1], [1, 2], [2, 5], [0, 3], [3, 4], [4, 5]]
assert path_exists(6, links, 0, 5, lambda x: x in {2}) is True
assert path_exists(6, links, 0, 5, lambda x: x in {2, 4}) is False
assert path_exists(6, links, 0, 0, lambda x: False) is True
assert path_exists(6, links, 0, 5, lambda x: x == 0) is False

"""
"""
def valid_palindrom(s: str)->bool:
    left ,right = 0, len(s)-1
    while left<right:
        if not s[left].isalnum():
            left += 1
            continue
        if not s[right].isalnum():
            right -= 1
            continue
        if s[left].lower() != s[right].lower():
            return False
        left +=1
        right -= 1
    return True

"""
Cities are connected by one-way flights. Each flight is [from_city, to_city, price].

Return the cheapest total price to get from src to dst, or -1 if dst can't be reached.
"""    
from collections import deque, defaultdict
def cheapest_route(flights: list[list[int]], src: int, dst: int) -> int:
    # Dijkstra: BFS with a min-heap (cheapest first) + a best-cost dict instead of a visited set
    import heapq
    graph = defaultdict(list)
    for frm, to, price in flights:
        graph[frm].append((to, price))          # one-way flights

    best = {src: 0}                             # city -> cheapest known cost
    heap = [(0, src)]                           # (cost so far, city)
    while heap:
        cost, city = heapq.heappop(heap)
        if city == dst:
            return cost                         # first time dst is popped = cheapest
        if cost > best[city]:
            continue                            # stale entry, a cheaper one was found
        for nxt, price in graph[city]:
            new_cost = cost + price
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(heap, (new_cost, nxt))
    return -1
# Time O(E log V), space O(V + E)

_flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500], [2, 3, 50]]
assert cheapest_route(_flights, 0, 2) == 200
assert cheapest_route(_flights, 0, 3) == 250
assert cheapest_route(_flights, 3, 0) == -1
assert cheapest_route(_flights, 1, 1) == 0
assert cheapest_route([], 0, 1) == -1
