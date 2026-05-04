from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data/patrol_request.json"


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/patrol")
def patrol_page():
    return render_template("patrol.html")


@app.route("/send", methods=["POST"])
def send():
    date = request.form.get("date")
    time = request.form.get("time")

    os.makedirs("data", exist_ok=True)

    with open("data/patrol_request.json", "w") as f:
        json.dump({
            "date": date,
            "time": time
        }, f)

    return render_template("send.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)