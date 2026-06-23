
from flask import Flask, request, jsonify, send_from_directory
import requests
import json
import os

app = Flask(__name__, static_folder='.', static_url_path='')

MAIL_API = "https://api.mail.tm"

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(endpoint):
  
    if request.method == 'OPTIONS':
        return '', 204
    
    target_url = f"{MAIL_API}/{endpoint}"
    
    if request.query_string:
        target_url += f"?{request.query_string.decode()}"
    
    try:
        
        headers = {}
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']
        if 'Content-Type' in request.headers:
            headers['Content-Type'] = request.headers['Content-Type']
        
        if request.method == 'POST':
            response = requests.post(
                target_url,
                json=request.get_json() if request.is_json else None,
                headers=headers,
                timeout=10
            )
        elif request.method == 'PUT':
            response = requests.put(
                target_url,
                json=request.get_json() if request.is_json else None,
                headers=headers,
                timeout=10
            )
        elif request.method == 'DELETE':
            response = requests.delete(
                target_url,
                headers=headers,
                timeout=10
            )
        elif request.method == 'PATCH':
            response = requests.patch(
                target_url,
                json=request.get_json() if request.is_json else None,
                headers=headers,
                timeout=10
            )
        else: 
            response = requests.get(
                target_url,
                headers=headers,
                timeout=10
            )
        
        try:
            return jsonify(response.json()), response.status_code
        except:
            return response.text, response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timeout"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    env = os.environ.get('FLASK_ENV', 'production')
    
    if env == 'development':
        print("Starting CORS Proxy Server (Development)...")
        print("Server running at http://127.0.0.1:5000")
        print("API endpoints proxied to: https://api.mail.tm")
        app.run(debug=False, host='127.0.0.1', port=5000)
    else:
        print(f"Starting CORS Proxy Server (Production on port {port})...")
        print("API endpoints proxied to: https://api.mail.tm")
        app.run(debug=False, host='0.0.0.0', port=port)
