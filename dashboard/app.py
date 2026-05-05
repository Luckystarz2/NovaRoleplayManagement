from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_API_URL = os.getenv("BOT_API_URL")  # MUST be Railway URL

# -------------------
# HOME
# -------------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/patrol")
def patrol():
    return render_template("patrol.html")

@app.route("/send")
def send():
    return render_template("send.html")

# -------------------
# STATUS API
# -------------------
@app.route("/api/status", methods=["POST"])
def set_status():
    data = request.json

    r = requests.post(f"{BOT_API_URL}/set-status", json=data)
    return jsonify(r.json())

# -------------------
# PATROL API
# -------------------
@app.route("/api/patrol", methods=["POST"])
def patrol_api():
    data = request.json

    r = requests.post(f"{BOT_API_URL}/patrol", json=data)
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)