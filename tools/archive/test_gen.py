"""Medium-length generation test."""
import sys, time, httpx

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
        {"role": "system", "content": "Write a detailed tutorial about Java constants."},
        {"role": "user", "content": "Write a 2000-word chapter section about Java constants including final keyword, static final, enum constants, and constant naming conventions. Include code examples."}
    ],
    "max_tokens": 4096,
    "temperature": 0.7,
}

sys.stderr.write("Generating medium text...\n")
sys.stderr.flush()
t0 = time.time()
try:
    with httpx.Client(timeout=300) as client:
        resp = client.post(f"{base_url}/chat/completions", headers=headers, json=payload)
        elapsed = time.time() - t0
        sys.stderr.write(f"Status: {resp.status_code}, Time: {elapsed:.1f}s\n")
        if resp.status_code == 200:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            sys.stdout.write(f"OK|{len(content)} chars|{elapsed:.1f}s\n")
        else:
            sys.stdout.write(f"FAIL|{resp.text[:200]}\n")
except Exception as e:
    elapsed = time.time() - t0
    sys.stdout.write(f"ERROR|{elapsed:.1f}s|{e}\n")
