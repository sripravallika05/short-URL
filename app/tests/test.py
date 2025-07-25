import json

def test_health(client):
    resp = client.get('/api/health')
    assert resp.status_code == 200
    assert resp.json["status"] == "ok"

def test_shorten_and_redirect(client):
    # Shorten
    resp = client.post('/api/shorten', json={"url": "https://example.com"})
    assert resp.status_code == 201
    data = resp.get_json()
    short_code = data["short_code"]

    # Redirect
    resp = client.get(f'/{short_code}', follow_redirects=False)
    assert resp.status_code == 302
    assert "example.com" in resp.headers["Location"]

def test_invalid_url(client):
    resp = client.post('/api/shorten', json={"url": "invalid-url"})
    assert resp.status_code == 400

def test_stats(client):
    # Shorten
    resp = client.post('/api/shorten', json={"url": "https://google.com"})
    short_code = resp.json["short_code"]

    # Access the short URL
    client.get(f'/{short_code}')
    client.get(f'/{short_code}')

    # Stats
    resp = client.get(f'/api/stats/{short_code}')
    assert resp.status_code == 200
    data = resp.json
    assert data["url"] == "https://google.com"
    assert data["clicks"] == 2
