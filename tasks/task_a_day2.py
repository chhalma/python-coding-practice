RAW = [
    {"txn_id": "t1", "account": "ACC1", "amount": "100.50"},
    {"txn_id": "t2", "account": "ACC2", "amount": "250"},
    {"txn_id": "t1", "account": "ACC1", "amount": "100.50"},
    {"txn_id": "t3", "account": "ACC1", "amount": "abc"},
    {"txn_id": "t4", "amount": "75"},
    {"txn_id": "t5", "account": "ACC2", "amount": "-20"},
    {"txn_id": "t6", "account": "ACC3", "amount": "0"},
]
""""
Write process(transactions: list[dict]) -> dict that:

Validates each transaction. It needs txn_id, account and amount, and amount has to parse as a number.
Deduplicates by txn_id.
Totals the valid amounts per account.
Returns:
totals per account, sorted by total descending
rejection counts by reason

"""
##So my undestanding is i nned to reeturn total per account for all the valid transactions. and also rejection count per reason. in this process i need to dedup the duplicate transactions.
## It will also consider extra fied 
REQUIRED_FIELDS = ("txn_id", "account", "amount")
    
def validate_transaction(trans:dict)->tuple[str,str,float]:
    extra =  trans.keys() - set(REQUIRED_FIELDS)
    missing = set(REQUIRED_FIELDS) -trans.keys()
    if extra:
        return None, "unexpected_field"
    if missing:
        return None, "missing_field"
    
    else:
        amount = trans.get('amount')
        try:
            flt_amount = float(amount)
        except (ValueError,TypeError):
            return None, "invalid_amount"
        else:
            txn_id = trans.get('txn_id')
            account = trans.get('account')
            return (txn_id,account,flt_amount), None


from collections import defaultdict, Counter
def process(transactions: list[dict])-> dict:
    seen_ids = set()
    results = defaultdict(float)
    rejection = Counter()
    for t in transactions:
        res,reason =  validate_transaction(t)
        if res is None:
            rejection[reason] += 1
            continue
        txn_id, account, amount = res
        if txn_id in seen_ids:
            rejection["duplicate"] += 1
            continue
        seen_ids.add(txn_id)
        results[account] += amount

    sorted_res = sorted(results.items(),key = lambda kv:(-kv[1]))
    return {"totals": dict(sorted_res), "rejected": dict(rejection)}



if __name__ == "__main__":
    print(process(RAW))
    
