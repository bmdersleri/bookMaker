"""Test retry + backoff mekanizmasi."""
import sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from bookmaker.llm.openai import OpenAICompatibleClient

client = OpenAICompatibleClient(
    api_key="sk-98a85ecced414d499d34caf73a09b80d",
    model="deepseek-chat",
    timeout=120,
    max_retries=3,
    retry_delay=2.0,
)

# Test 1: Quick connection test
print("=== Test 1: Baglanti testi ===")
start = time.time()
result = client.test_connection()
elapsed = time.time() - start
retries = result.get("retries", "N/A")
print(f"Status: {result['status']}, Retries: {retries}, Time: {elapsed:.1f}s")

# Test 2: Text generation
print()
print("=== Test 2: Metin uretimi ===")
start = time.time()
try:
    text = client.generate_text(
        "Sen bir Java egitmenisin.",
        "2 cumleyle Javanin temel ozelliklerini anlat.",
        max_tokens=100,
    )
    elapsed = time.time() - start
    print(f"OK ({elapsed:.1f}s): {len(text)} chars")
    print(text[:200])
except RuntimeError as e:
    elapsed = time.time() - start
    print(f"ERROR ({elapsed:.1f}s): {e}")

print()
print("Retry mekanizmasi hazir!")
