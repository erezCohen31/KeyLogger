from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})

# Directory to save the uploaded files
SAVE_DIR = "received_files"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_json():
    """Receives a JSON file and stores it"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON file received"}), 400

        file_path = os.path.join(SAVE_DIR, "received_data.json")

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        return jsonify({"message": "JSON file received successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download', methods=['GET'])
def download_json():
    """Retrieves and returns the JSON file"""
    try:
        file_path = os.path.join(SAVE_DIR, "received_data.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
            return jsonify(data), 200
        else:
            return jsonify({"error": "The JSON file does not exist"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
