"""Static mount dogrulama + servis testleri."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'src')

from fastapi.testclient import TestClient
from bookmaker.studio.app import app

client = TestClient(app)

# 1. STATIC MOUNT
print("=== STATIC MOUNT TEST ===")
for path, label in [('/static/styles.css', 'CSS'), ('/static/app.js', 'JS')]:
    r = client.get(path)
    if r.status_code == 200 and len(r.text) > 500:
        print(f"  OK {label}: {len(r.text):,} bytes yuklendi")
    else:
        print(f"  FAIL {label}: status={r.status_code}, size={len(r.text)}")

# 2. INDEX.HTML STATIC LINK KONTROLU
r = client.get('/')
has_css = '/static/styles.css' in r.text
has_js = '/static/app.js' in r.text
print(f"  index.html -> styles.css: {'OK' if has_css else 'MISSING'}")
print(f"  index.html -> app.js: {'OK' if has_js else 'MISSING'}")
print(f"  Dashboard boyut: {len(r.text):,} bytes")

# 3. API ENDPOINTS QUICK CHECK
print("\n=== API ENDPOINTS ===")
for path in ['/api/status', '/api/project', '/api/chapters', '/api/llm-status',
             '/api/pipeline-state', '/api/jobs']:
    r = client.get(path)
    status = 'OK' if r.status_code == 200 else f'FAIL {r.status_code}'
    print(f"  {status}: {path}")

print("\nFaz 1 eksik testlerin tamami!")
