"""
Refresh 5 — AI-flavoured coding problems (plain Python, no libraries needed).
Fill in each function body (replace `raise NotImplementedError`), then run the file:
each test prints PASS / FAIL / TODO / ERROR.
Say out loud for each: the approach, edge cases, and time/space complexity.
"""
import heapq
import json
import math
from collections import Counter


# 1. Chunk text with overlap (~15 min) — RAG preprocessing
# Split `words` into chunks of `size` words; each chunk starts `size - overlap` words after the previous.
# Raise ValueError if size <= 0 or overlap < 0 or overlap >= size.
#   chunk_words(["a","b","c","d","e"], size=3, overlap=1) -> [["a","b","c"], ["c","d","e"]]
def chunk_words(words: list[str], size: int, overlap: int) -> list[list[str]]:
    if size <=0 or overlap <0 or overlap >= size:
        raise ValueError(f"invalid size={size}, overlap={overlap}")
    result = []
    for i in range(0,len(words),size-overlap):
        word = words[i:i+size]
        result.append(word)
        if i+size >= len(words):
            break
    return result



# 2. Cosine similarity (~10 min)
# cos(a, b) = dot(a, b) / (|a| * |b|). Return 0.0 if either vector has zero length (avoid division by zero).
# Raise ValueError if the vectors have different lengths.
#   cosine([1, 0], [1, 0]) -> 1.0       cosine([1, 0], [0, 1]) -> 0.0
def cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError(f"length mismatch: {len(a)} vs {len(b)}")

    dot = sum(x*y for x,y in zip(a,b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(y*y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot/(norm_a*norm_b)
    

# 3. Top-k retrieval (~15 min) — the "R" in RAG
# docs = {doc_id: vector}. Return the k doc_ids most similar to `query`, best first.
# Ties: smaller doc_id first. Use heapq or sorted — say which and why.
#   top_k([1, 0], {"d1": [1, 0], "d2": [0, 1], "d3": [1, 1]}, k=2) -> ["d1", "d3"]
def top_k(query: list[float], docs: dict[str, list[float]], k: int) -> list[str]:
    scores = {id:cosine(query, b) for id, b in docs.items()}
    best = heapq.nsmallest(k, scores.items(),key = lambda kv: (-kv[1],kv[0] ))
    return [doc_id for doc_id,_ in best]

# 4. Precision / recall / F1 for sets (~15 min) — evaluating extraction or retrieval
# predicted vs expected are sets of labels. Return (precision, recall, f1), each rounded to 2 dp.
# Define: if predicted is empty -> precision 1.0 when expected is also empty, else 0.0 (same idea for recall).
#   prf({"Cyber", "Property"}, {"Cyber", "D&O"}) -> (0.5, 0.5, 0.5)
def prf(predicted: set[str], expected: set[str]) -> tuple[float, float, float]:
    tp = len(predicted & expected)
    fp = len(predicted - expected)
    fn = len(expected - predicted)
    
    if tp+fp >0:
        precision = tp/(tp+fp)
    else:
        precision =1.0 if not expected else 0.0
    if tp+fn >0:
        recall = tp/(tp+fn)
    else:
        recall =1.0 if not predicted else 0.0

    f1 = (2*precision*recall)/(precision+recall) if precision+recall > 0 else 0.0

    return (round(precision,2),round(recall,2),round(f1,2)) 

# 5. Validate LLM JSON output (~20 min)
# The LLM should return JSON like {"company_name": str, "revenue": int, "countries": [str, ...]}.
# Return (record, errors): record is the parsed dict if valid, else None; errors is a list of messages.
# Check: valid JSON, all 3 keys present, correct types, revenue >= 0.
#   validate_llm_output('{"company_name": "Acme Ltd", "revenue": 500, "countries": ["UK"]}')
#     -> ({"company_name": "Acme Ltd", "revenue": 500, "countries": ["UK"]}, [])

REQUIRED_TYPES = {"company_name": str, "revenue": int, "countries": list}

def validate_llm_output(raw: str) -> tuple[dict | None, list[str]]:
    try:
        data =  json.loads(raw)
    except json.JSONDecodeError:
        return None , ["invalid JSON"]
    if not isinstance(data, dict):
        return None, ["expected a JSON object"]
    errors = []
    for key, expected_type in REQUIRED_TYPES.items():
        if key not in data:
            errors.append(f"missing field: {key}")
        elif not isinstance(data[key], expected_type) or isinstance(data[key], bool):
            errors.append(f"{key} should be {expected_type.__name__},,got {type(data[key]).__name__}")
    revenue =  data.get("revenue")
    if isinstance(revenue,int) and not isinstance(revenue,bool) and revenue <0:
        errors.append(f"revenue must be >= 0, got {revenue}")

    return (None if errors else data),errors        
# 6. Retry with fallback (~15 min)
# Call each function in `providers` in order. If one raises an exception, retry it up to `max_retries`
# extra times, then move on to the next provider. Return the first successful result.
# If every provider fails, raise RuntimeError. (No sleeping needed — just count attempts.)
#   call_with_fallback([flaky_fails_twice, backup], max_retries=2) -> result of flaky on its 3rd attempt
def call_with_fallback(providers: list, max_retries: int):
    errors = []
    for provider in providers:
        for attempt in range(1, max_retries+2):
            try:
                return provider()
            except Exception as e:
                errors.append(f"{getattr(provider, '__name__', 'provider')} attempt {attempt}:{e}" )
    raise RuntimeError(f"all providers failed after retries:{errors}")

# 7. Keyword search over chunks (~15 min) — a no-embeddings baseline retriever
# Score each chunk by how many times the query's words appear in it (case-insensitive).
# Return the index of the best-scoring chunk; ties -> lower index; if every score is 0, return -1.
#   best_chunk("cyber cover", ["property schedule", "cyber and cyber cover", "cover note"]) -> 1
def best_chunk(query: str, chunks: list[str]) -> int:
    query_words = query.lower().split()
    best_index, best_score = -1, 0

    for i, chunk in enumerate(chunks):
        chunk_count = Counter(chunk.lower().split()) 
        score = sum(chunk_count[word] for word in query_words)
        if score > best_score:
            best_index,best_score = i, score
    return best_index
# ---------------------------------------------------------------- tests
def _raises(fn, exc) -> bool:
    try:
        fn()
    except exc:
        return True
    return False


def _flaky(failures: int, result: str):
    """A provider that fails `failures` times, then returns `result`."""
    state = {"calls": 0}

    def provider():
        state["calls"] += 1
        if state["calls"] <= failures:
            raise TimeoutError("simulated timeout")
        return result
    return provider


def _tests() -> dict:
    return {
        "1 chunk_words": lambda: (
            chunk_words(list("abcde"), 3, 1) == [["a", "b", "c"], ["c", "d", "e"]]
            and chunk_words(list("abcdef"), 3, 1) == [["a", "b", "c"], ["c", "d", "e"], ["e", "f"]]
            and chunk_words(list("ab"), 3, 1) == [["a", "b"]]
            and chunk_words([], 3, 1) == []
            and _raises(lambda: chunk_words(list("abc"), 2, 2), ValueError)
        ),
        "2 cosine": lambda: (
            cosine([1, 0], [1, 0]) == 1.0
            and cosine([1, 0], [0, 1]) == 0.0
            and round(cosine([1, 1], [1, 0]), 4) == 0.7071
            and cosine([0, 0], [1, 1]) == 0.0
            and _raises(lambda: cosine([1], [1, 2]), ValueError)
        ),
        "3 top_k": lambda: (
            top_k([1, 0], {"d1": [1, 0], "d2": [0, 1], "d3": [1, 1]}, 2) == ["d1", "d3"]
            and top_k([1, 0], {"b": [1, 0], "a": [2, 0]}, 2) == ["a", "b"]
            and top_k([1, 0], {"d1": [1, 0]}, 5) == ["d1"]
            and top_k([1, 0], {}, 3) == []
        ),
        "4 prf": lambda: (
            prf({"Cyber", "Property"}, {"Cyber", "D&O"}) == (0.5, 0.5, 0.5)
            and prf({"Cyber"}, {"Cyber", "D&O"}) == (1.0, 0.5, 0.67)
            and prf(set(), set()) == (1.0, 1.0, 1.0)
            and prf(set(), {"Cyber"}) == (0.0, 0.0, 0.0)
        ),
        "5 validate_llm_output": lambda: (
            validate_llm_output('{"company_name": "Acme Ltd", "revenue": 500, "countries": ["UK"]}')
            == ({"company_name": "Acme Ltd", "revenue": 500, "countries": ["UK"]}, [])
            and validate_llm_output("not json")[0] is None
            and validate_llm_output('{"company_name": "Acme"}')[0] is None
            and validate_llm_output('{"company_name": "A", "revenue": "500", "countries": []}')[0] is None
            and validate_llm_output('{"company_name": "A", "revenue": -1, "countries": []}')[0] is None
            and len(validate_llm_output('{"company_name": 1, "revenue": "x", "countries": "UK"}')[1]) >= 3
        ),
        "6 call_with_fallback": lambda: (
            call_with_fallback([_flaky(2, "primary")], max_retries=2) == "primary"
            and call_with_fallback([_flaky(5, "primary"), _flaky(0, "backup")], max_retries=2) == "backup"
            and _raises(lambda: call_with_fallback([_flaky(9, "x")], max_retries=1), RuntimeError)
        ),
        "7 best_chunk": lambda: (
            best_chunk("cyber cover", ["property schedule", "cyber and cyber cover", "cover note"]) == 1
            and best_chunk("CYBER", ["cyber", "Cyber"]) == 0
            and best_chunk("marine", ["property", "cyber"]) == -1
            and best_chunk("x", []) == -1
        ),
    }


if __name__ == "__main__":
    for name, test in _tests().items():
        try:
            print(f"{'PASS' if test() else 'FAIL'}  {name}")
        except NotImplementedError:
            print(f"TODO  {name}")
        except Exception as e:
            print(f"ERROR {name}: {type(e).__name__}: {e}")
