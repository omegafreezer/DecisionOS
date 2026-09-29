from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health'); assert r.status_code == 200; assert r.json()['status'] == 'ok'

def test_summary():
    r = client.get('/api/summary'); assert r.status_code == 200; assert r.json()['total_revenue'] > 0

def test_scenario():
    r = client.post('/api/simulate', json={'inventory_delta':0.15,'price_delta':0,'marketing_delta':0}); assert r.status_code == 200; assert 'projected_daily_revenue' in r.json()['result']['evidence'][0]
