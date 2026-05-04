from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_API = os.getenv("BOT_API_URL", "http://localhost:5001")


# -------------------------
# PAGES
# -------------------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/patrol")
def patrol():
    return render_template("patrol.html")


@app.route("/send")
def send():
    return render_template("send.html")


# -------------------------
# BOT STATUS
# -------------------------
@app.route("/api/status")
def status():
    try:
        r = requests.get(f"{BOT_API}/status")
        return jsonify(r.json())
    except:
        return jsonify({"online": False})


# -------------------------
# UPDATE STATUS
# -------------------------
@app.route("/api/status/set", methods=["POST"])
def set_status():
    try:
        r = requests.post(
            f"{BOT_API}/status/set",
            json=request.json
        )
        return jsonify(r.json())
    except:
        return jsonify({"success": False})


# -------------------------
# SEND MESSAGE
# -------------------------
@app.route("/api/send", methods=["POST"])
def send_msg():
    try:
        r = requests.post(
            f"{BOT_API}/send",
            json=request.json
        )
        return jsonify(r.json())
    except:
        return jsonify({"success": False})


# -------------------------
# PATROL CREATE
# -------------------------
@app.route("/api/patrol/create", methods=["POST"])
def patrol_create():
    try:
        r = requests.post(
            f"{BOT_API}/patrol/create",
            json=request.json
        )
        return jsonify(r.json())
    except:
        return jsonify({"success": False})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)