import pytest
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'

def test_shorten_and_redirect(client):
    url = "https://example.com/test"
    response = client.post('/api/shorten', json={"url": url})
    assert response.status_code == 201
    data = response.get_json()
    short_code = data['short_code']

    redirect_response = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_response.status_code == 302
    assert redirect_response.location == url

def test_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "not-a-valid-url"})
    assert response.status_code == 400

def test_missing_url_field(client):
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400

def test_stats(client):
    url = "https://example.com/stats"
    response = client.post('/api/shorten', json={"url": url})
    short_code = response.get_json()['short_code']

    # Trigger some clicks
    client.get(f"/{short_code}")
    client.get(f"/{short_code}")

    stats_response = client.get(f"/api/stats/{short_code}")
    stats_data = stats_response.get_json()

    assert stats_data['url'] == url
    assert stats_data['clicks'] == 2
    assert "created_at" in stats_data
