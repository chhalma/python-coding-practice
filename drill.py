def average(total: float, count: int) -> float:
    if count == 0:
        return 0.0
    return total / count          


def report(values: list[float]) -> None:
    avg = average(sum(values), len(values))
    print(f"Average: {avg}")


if __name__ == "__main__":
    report([10,20,30])
    report([])
