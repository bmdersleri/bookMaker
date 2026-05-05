"""Verify index.html with static file links."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, 'src')
from fastapi.testclient import TestClient
from bookmaker.studio.app import app

client = TestClient(app)
r = client.get('/')
html = r.text

print(f'index.html: {len(html):,} chars')
print(f'Contains styles.css link: {"/static/styles.css" in html}')
print(f'Contains app.js link: {"/static/app.js" in html}')
print(f'Contains bookMaker: {"bookMaker" in html}')
print(f'Contains Bolum: {"Bolum" in html}')
print(f'Status: {r.status_code}')
