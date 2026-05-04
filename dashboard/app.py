from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_API_URL = os.getenv("BOT_API_URL", "http://localhost:5001")

# -------------------
# DASHBOARD PAGES
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
# API: SET STATUS
# -------------------
@app.route("/api/status", methods=["POST"])
def set_status():
    data = request.json

    try:
        r = requests.post(f"{BOT_API_URL}/set-status", json=data)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})


# -------------------
# API: SEND PATROL
# -------------------
@app.route("/api/patrol", methods=["POST"])
def send_patrol():
    data = request.json

    try:
        r = requests.post(f"{BOT_API_URL}/patrol", json=data)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)