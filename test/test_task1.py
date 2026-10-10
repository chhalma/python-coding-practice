from tasks.task1 import summarise,LINES


def test_sample_lines():
    result = summarise(LINES)
    assert result["skipped"] == 1
    assert result["paths"]["/api/jobs"] == {"count": 3, "error_rate": 0.33, "avg_latency_ms": 185.0}
    assert result["paths"]["/api/users"] == {"count": 1, "error_rate": 0.0, "avg_latency_ms": 30.0}

def test_empty_input():
    assert summarise([]) == {"paths":{},"skipped":0}
    
def test_too_few_fields():
    assert summarise(["this is a bad"]) == {"paths":{},"skipped":1}
def test_too_many_fields():
    assert summarise(["this is a bad bad very bad"]) == {"paths":{},"skipped":1}

def test_wrong_type():
    assert summarise(["20-11-2026 Get /api/jobs hello world"]) == {"paths":{}, "skipped":1}