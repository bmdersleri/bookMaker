"""Quick manual test of live Studio server."""
import requests, sys

BASE = "http://127.0.0.1:8765"

def test(path):
    r = requests.get(f"{BASE}{path}", timeout=5)
    data = r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text[:200]
    print(f"  GET {path:30s} {r.status_code:>3d}  {str(data)[:80]}")
    return r

print("Testing Studio server...")
r = test("/")
assert "bookMaker" in str(r.text), "Dashboard not rendering"
print(f"     Dashboard size: {len(r.text):,} bytes")

r = test("/api/status")
test("/api/project")
test("/api/chapters")
test("/api/llm-status")
test("/api/pipeline-state")

# Test a real chapter check
r = test("/api/check/bolum-01")
d = r.json()
if "score" in d:
    print(f"     Score: {d['score']}, Decision: {d['decision']}")

print("\n✅ Studio çalışıyor: http://127.0.0.1:8765")
