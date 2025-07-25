from flask import Flask, request, jsonify, redirect
from app.storage import URLStorage
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)
storage = URLStorage()

@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "service": "URL Shortener API"})

@app.route('/api/health')
def api_health():
    return jsonify({"status": "ok", "message": "URL Shortener API is running"})

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    url = data["url"]
    if not is_valid_url(url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    storage.save_url(short_code, url)

    return jsonify({
        "short_code": short_code,
        "short_url": request.host_url + short_code
    }), 201

@app.route('/<short_code>')
def redirect_to_url(short_code):
    record = storage.get_url(short_code)
    if not record:
        return jsonify({"error": "Short URL not found"}), 404

    storage.increment_click(short_code)
    return redirect(record["url"])

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    record = storage.get_stats(short_code)
    if not record:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "url": record["url"],
        "clicks": record["clicks"],
        "created_at": record["created_at"]
    })
