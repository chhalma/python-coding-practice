"""
You receive a list of user records. Write a function get_valid_emails(users) that returns the email addresses of users who are active and have a valid email field.
expected Output : ["a@example.com", "d@example.com"]

"""
users = [
    {"name": "A", "email": "a@example.com", "active": True},
    {"name": "B", "email": "b@example.com", "active": False},
    {"name": "C", "email": None, "active": True},
    {"name": "D", "email": "d@example.com", "active": True},
    {"name": "E", "email": "", "active": True},
]

import re

def get_valid_emails1(users:list[dict])->list:
    EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w]+(\.[\w]+)+$")
    valid_active_email = []
    for user in users:
        email = user.get("email")
        status =  user.get("active")
        if isinstance(email,str) and EMAIL_PATTERN.fullmatch(email) and status == True:
            valid_active_email.append(email)
    return valid_active_email
def get_valid_emails(users:list[dict])->list:
    
    valid_active_email = []
    for user in users:
        email = user.get("email")
        status =  user.get("active")
        if status == True and isinstance(email,str) and email and email.count('@') == 1 :
            valid_active_email.append(email)
    return valid_active_email


assert get_valid_emails(users) == ["a@example.com", "d@example.com"]
## time: O(n) space: O(n)

"""
Given a list of integers, return the second-largest distinct value. If fewer than two distinct values exist, return None.
    second_largest([4, 1, 7, 7, 3])  # 4
    second_largest([5, 5])          # None
    second_largest([-1, -3, -2])    # -2
    second_largest([])              # None
"""
import heapq
def second_largest(nums:list)->int:
    if not nums:
        return None
    heap = []
    dic_num = set(nums)
    for n in dic_num:
        heapq.heappush(heap,n)
        if len(heap)>2:
            heapq.heappop(heap)
    return heap[0] if len(heap) == 2 else None

assert second_largest([2,4,1,6,7]) == 6
assert second_largest([4,5,6,7,7,7]) == 6
assert second_largest([-1, -3, -2])  == -2
assert second_largest([5, 5])  == None