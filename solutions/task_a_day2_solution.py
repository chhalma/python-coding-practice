from collections import Counter, defaultdict  # FIX: imports at the top

RAW = [
    {"txn_id": "t1", "account": "ACC1", "amount": "100.50"},
    {"txn_id": "t2", "account": "ACC2", "amount": "250"},
    {"txn_id": "t1", "account": "ACC1", "amount": "100.50"},
    {"txn_id": "t3", "account": "ACC1", "amount": "abc"},
    {"txn_id": "t4", "amount": "75"},
    {"txn_id": "t5", "account": "ACC2", "amount": "-20"},
    {"txn_id": "t6", "account": "ACC3", "amount": "0"},
]
"""
Write process(transactions: list[dict]) -> dict that:

Validates each transaction. It needs txn_id, account and amount, and amount has to parse as a number.
Deduplicates by txn_id.
Totals the valid amounts per account.
Returns:
totals per account, sorted by total descending
rejection counts by reason
"""
## So my understanding is I need to return total per account for all the valid transactions, and also
## rejection count per reason. In this process I need to dedup the duplicate transactions.
##
## Assumptions (would ask the interviewer):
##   - Duplicate = same txn_id; the FIRST one wins, later ones are rejected as "duplicate".
##   - Negative amounts are refunds -> valid. Zero is valid.
##   - Order of checks: missing field -> invalid amount -> duplicate.
##
## Expected for RAW (by hand):
##   totals:   ACC2 = 250 - 20 = 230.0, ACC1 = 100.5, ACC3 = 0.0
##   rejected: duplicate 1 (t1 again), invalid_amount 1 (t3), missing_field 1 (t4)

REQUIRED_FIELDS = ("txn_id", "account", "amount")


# FIX: return (parsed, reason) so the caller knows WHY it failed; exactly one of the two is None.
def validate_transaction(trans: dict) -> tuple[tuple[str, str, float] | None, str | None]:
    if any(field not in trans for field in REQUIRED_FIELDS):  # FIX: was `trans.keys not in [...]` (always True)
        return None, "missing_field"
    try:
        flt_amount = float(trans["amount"])
    except ValueError:
        return None, "invalid_amount"
    return (trans["txn_id"], trans["account"], flt_amount), None


def process(transactions: list[dict]) -> dict:  # FIX: name was `precess`
    seen_ids = set()
    results = defaultdict(float)
    rejections = Counter()  # FIX: counts per reason instead of one number
    for t in transactions:
        res, reason = validate_transaction(t)
        if res is None:
            rejections[reason] += 1
            continue
        txn_id, account, amount = res
        if txn_id in seen_ids:
            rejections["duplicate"] += 1  # FIX: duplicates are rejections too
            continue
        seen_ids.add(txn_id)
        results[account] += amount

    sorted_res = sorted(results.items(), key=lambda kv: (-kv[1], kv[0]))  # FIX: tie-break by account
    return {"totals": dict(sorted_res), "rejected": dict(rejections)}


# --- tests ---
result = process(RAW)
assert result["totals"] == {"ACC2": 230.0, "ACC1": 100.5, "ACC3": 0.0}
assert list(result["totals"]) == ["ACC2", "ACC1", "ACC3"]  # order matters: descending
assert result["rejected"] == {"duplicate": 1, "invalid_amount": 1, "missing_field": 1}

assert process([]) == {"totals": {}, "rejected": {}}
assert process([{"txn_id": "x", "amount": "5"}])["rejected"] == {"missing_field": 1}
assert process([{"txn_id": "x", "account": "A", "amount": "abc"}])["rejected"] == {"invalid_amount": 1}

print(result)
print("all tests passed")

# Complexity: O(n) to validate/dedup/accumulate (set + dict lookups are O(1)),
#             O(a log a) to sort a accounts. Space O(n) for seen_ids + O(a) for totals.
# Improvements:
#   - Use Decimal instead of float for money (0.1 + 0.2 != 0.3).
#   - Reject "nan"/"inf" amounts (float() accepts them) with math.isfinite.
#   - Return the rejected txn_ids too, not just counts, so someone can investigate.
