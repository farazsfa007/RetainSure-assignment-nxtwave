from flask import Flask, request, jsonify, redirect
from app.models import save_url_mapping, get_original_url, increment_click, get_stats
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)
BASE_URL = "http://localhost:5000"

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' field"}), 400

    long_url = data['url']
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL format"}), 400

    short_code = generate_short_code()
    save_url_mapping(short_code, long_url)
    return jsonify({
        "short_code": short_code,
        "short_url": f"{BASE_URL}/{short_code}"
    }), 201

@app.route('/<short_code>')
def redirect_to_url(short_code):
    data = get_original_url(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404
    increment_click(short_code)
    return redirect(data["original_url"])

@app.route('/api/stats/<short_code>')
def stats(short_code):
    data = get_stats(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404
    return jsonify({
        "url": data["original_url"],
        "clicks": data["clicks"],
        "created_at": data["created_at"]
    })
