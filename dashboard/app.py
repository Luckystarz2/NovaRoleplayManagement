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
# RESTART BOT
# -------------------------
@app.route("/api/restart", methods=["POST"])
def restart():
    try:
        r = requests.post(f"{BOT_API}/restart")
        return jsonify(r.json())
    except:
        return jsonify({"success": False})


# -------------------------
# CHANGE STATUS
# -------------------------
@app.route("/api/status/set", methods=["POST"])
def set_status():
    data = request.json

    try:
        r = requests.post(
            f"{BOT_API}/status/set",
            json={
                "type": data.get("type"),
                "text": data.get("text")
            }
        )
        return jsonify(r.json())
    except:
        return jsonify({"success": False})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)