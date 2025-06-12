from flask import Flask, request, jsonify
from flask_cors import CORS  # Add CORS support
import secrets
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get port from environment or default to 10000
port = int(os.environ.get("PORT", 10000))

# Use environment variable for secret key
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(16))
codes = {}

@app.route('/generate', methods=['GET'])
def generate_code():
    code = secrets.token_hex(3).upper()  # 6-character code
    expiration = datetime.now() + timedelta(minutes=5)
    codes[code] = {
        "valid": True,
        "expires": expiration.timestamp()
    }
    print(f"Generated code: {code}")  # For Render log viewing
    return jsonify({"code": code})

@app.route('/verify', methods=['POST'])
def verify_code():
    data = request.get_json()
    code = data.get('code', '').strip().upper()
    
    if code in codes:
        if datetime.now().timestamp() < codes[code]["expires"]:
            if codes[code]["valid"]:
                codes[code]["valid"] = False  # Invalidate after use
                print(f"Verified code: {code}")
                return jsonify({"valid": True})
    print(f"Failed verification for: {code}")
    return jsonify({"valid": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)