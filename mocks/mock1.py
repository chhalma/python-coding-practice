from collections import defaultdict

def find_suspicious(lines: list[str], threshold: int = 3, window: int = 60) -> list[str]:
    errors = []
    suspicious = []
    summary = defaultdict(list)
    for line in lines:
        groups = line.split(',')
        if len(groups) <3:
            errors.append("not enough fields")
        else:
            time, account, amount = line.split(',')
            summary[account].append(int(time))
    for acc, times in  summary.items():
        sorted_times = sorted(times)
        count = 0
        left = 0
        for i,time in enumerate(sorted_times):
            diff = time - sorted_times[left]
            count += 1
            if count >= threshold and diff <= window:
                suspicious.append(acc)
                break
            elif diff > window:
                left += 1
                count -= 1

    return suspicious
  
            
LINES = [
    "100,ACC1,50.0",
    "130,ACC1,20.0",
    "150,ACC1,10.0",
    "100,ACC2,5.0",
    "200,ACC2,5.0",
    "250,ACC2,5.0",
    "bad line",
    "300,ACC3,1.0",
    "240,ACC3,1.0",
    "270,ACC3,1.0",
]
find_suspicious(LINES)

assert find_suspicious(LINES) == ["ACC1", "ACC3"]
print("mock1 passed")
