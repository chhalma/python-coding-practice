from tasks.task_a_day2 import process, RAW

def test_sample_input():
    result =  process(RAW)
    assert result["totals"]["ACC2"] == 230.0

def test_extra_field():
    tr = [{"txn_id": "t1", "account": "ACC1", "amount": "100.50", "Note": "Good"}]
        
    result = process(tr)
    assert result["rejected"] == {"unexpected_field":1}
    assert result["totals"] == {}

def test_empty_list():
    tr = []
        
    result = process(tr)
    assert result["rejected"] == {}
    assert result["totals"] == {}

def test_missing_field():
    tr = [{"txn_id": "t1", "account": "ACC1"}]
            
    result = process(tr)
    assert result["rejected"] == {"missing_field":1}
    assert result["totals"] == {}
def test_invalid_amount_is_rejected():
    tr = [{"txn_id": "t1", "account": "ACC1", "amount": "100.50d"}]
            
    result = process(tr)
    assert result["rejected"] == {"invalid_amount":1}
    assert result["totals"] == {}

def test_none_amount_is_rejected():
    tr = [{"txn_id": "t1", "account": "ACC1", "amount": None}]
        
        
    result = process(tr)
    assert result["rejected"] == {"invalid_amount":1}
    assert result["totals"] == {}
def test_deduplicated_rejected():
    tr = [{"txn_id": "t1", "account": "ACC1", "amount": "100"},{"txn_id": "t1", "account": "ACC1", "amount": "100"}]
        
        
    result = process(tr)
    assert result["rejected"] == {"duplicate":1}
    assert result["totals"] == {"ACC1": 100.0}