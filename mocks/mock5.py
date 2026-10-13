"""
Merge Intervals
Target: 8 minutes · Medium
Merge all overlapping intervals and return the merged intervals in sorted order.
Example: [[1,3], [2,6], [8,10], [15,18]] → [[1,6], [8,10], [15,18]]
"""
def merge_interval(intervals:list[list[int]])->list[list[int]]:
    intervals.sort()
    results = []
    results.append(intervals[0])
    for interval in intervals:
        start, end = interval
        if start <= results[-1][1]:
            results[-1][1] =  max(results[-1][1], end)
        else:
            results.append(interval)
    return results

assert merge_interval([[1,3], [2,6], [8,10], [15,18]] ) == [[1,6], [8,10], [15,18]]
        

"""

Longest Substring Without Repeating Characters
Target: 8 minutes · Medium
Return the length of the longest substring containing no repeated characters.
Example: "pwwkew" → 3



6

Meeting Rooms II
Target: 10 minutes · Medium
Given meeting intervals [[start, end], ...], return the minimum number of rooms required.
Example: [[0,30], [5,10], [15,20]] → 2
"""