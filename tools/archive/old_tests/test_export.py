"""Test export endpoints."""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'src')

from fastapi.testclient import TestClient
from bookmaker.studio.app import app

client = TestClient(app)

for path, label in [
    ('/api/assemble', 'Assemble'),
    ('/api/backup', 'Backup'),
    ('/api/extract', 'Extract'),
]:
    r = client.post(path, json={})
    d = r.json()
    err = d.get('error', '')
    status = f'FAIL: {err[:80]}' if err else f'OK: {d}'
    print(f'  {label}: {status}')
