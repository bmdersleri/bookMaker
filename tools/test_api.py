"""API baglanti testi - detayli."""
import sys, json, time, httpx

api_key = "sk-98a85ecced414d499d34caf73a09b80d"
base_url = "https://api.deepseek.com/v1"
model = "deepseek-chat"

for timeout in [30, 60, 120, 300]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Reply with only the word OK."}],
        "max_tokens": 10,
    }
    sys.stderr.write(f"Test timeout={timeout}... ")
    sys.stderr.flush()
    t0 = time.time()
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(f"{base_url}/chat/completions", headers=headers, json=payload)
            elapsed = time.time() - t0
            sys.stderr.write(f"status={resp.status_code} elapsed={elapsed:.1f}s\n")
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                sys.stdout.write(f"OK:{elapsed:.1f}s|{content}\n")
                sys.stdout.flush()
                sys.exit(0)
            else:
                sys.stderr.write(f"Error: {resp.text[:200]}\n")
    except Exception as e:
        elapsed = time.time() - t0
        sys.stderr.write(f"FAIL after {elapsed:.1f}s: {e}\n")

sys.stdout.write("ALL TIMEOUTS FAILED\n")
sys.exit(1)
