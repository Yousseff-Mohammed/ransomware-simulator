# 🔐 Ransomware Simulator (Educational Red Team Project)

## 🚨 Disclaimer

> ⚠️ **This project is for educational and ethical Red Team training only.**  
> Do **not** use this tool on any system without **explicit authorization**.  
> The author is not responsible for any misuse or damage caused by this code.

---

## 📌 Description

A Python-based ransomware simulator for **educational purposes**. This project demonstrates the core components of ransomware used by Red Teams to simulate real-world threats in controlled lab environments.

Key educational areas:
- File discovery and targeting
- Hybrid encryption (AES + RSA)
- Secure metadata logging
- Basic command-and-control communication via Flask

---

## 🎯 Features

- 🔍 **File Walker**: Finds target files based on extension
- 🔐 **AES (EAX Mode)**: Encrypts file contents
- 🔐 **RSA**: Encrypts AES key
- 📤 **Logger**: Sends encryption metadata to Flask C2 server
- 🖥️ **Flask C2 Server**: Simulated backend server
- 🔓 **Decryptor**: Safely decrypts files using RSA private key

---

## 📂 Project Structure

```plaintext
ransomware-simulator/
├── main.py                         # Entry point (optional / combined logic)
│
├── decryptor/
│   └── decryptor.py                # Decrypts files using RSA private key
│
├── encryptor/
│   ├── encryptor.py                # Handles AES file encryption
│   ├── file_walker.py              # Recursively finds target files
│   ├── rsa_key.py                  # RSA public key operations
│   ├── config.py                   # Global settings (paths, extensions, etc.)
│   └── keys/
│       └── public.pem              # RSA public key used for encryption
│
├── server/
│   ├── app.py                      # Flask-based C2 server + logs file metadata
│   └── keys/
│       └── private.pem             # RSA private key used for decryption



