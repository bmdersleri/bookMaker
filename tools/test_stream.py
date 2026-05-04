"""Streaming test to see if API is responding."""
import sys, time, httpx, json

api_key = "sk-98a85ecced414d499d34caf73a09b80d"
base_url = "https://api.deepseek.com/v1"
model = "deepseek-chat"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
payload = {
    "model": model,
    "messages": [
        {"role": "user", "content": "Write a paragraph about Java constants. Max 200 words."}
    ],
    "max_tokens": 500,
    "stream": True,
}

sys.stderr.write("Streaming test...\n")
sys.stderr.flush()
t0 = time.time()
try:
    with httpx.Client(timeout=120) as client:
        with client.stream("POST", f"{base_url}/chat/completions", headers=headers, json=payload) as resp:
            elapsed = time.time() - t0
            sys.stderr.write(f"Connected in {elapsed:.1f}s, status={resp.status_code}\n")
            sys.stderr.flush()
            chunks = 0
            for line in resp.iter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    chunks += 1
            elapsed2 = time.time() - t0
            sys.stderr.write(f"Done: {chunks} chunks in {elapsed2:.1f}s\n")
            sys.stdout.write(f"OK|{elapsed2:.1f}s|{chunks} chunks\n")
except Exception as e:
    elapsed = time.time() - t0
    sys.stdout.write(f"ERROR|{elapsed:.1f}s|{e}\n")
