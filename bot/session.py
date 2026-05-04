import json

SESSION_FILE = "data/session.json"

def load_session():
    with open(SESSION_FILE, "r") as f:
        return json.load(f)

def save_session(data):
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f, indent=4)

def start_session(players, ip):
    data = load_session()
    data["status"] = "SSU"
    data["players"] = players
    data["ip"] = ip
    save_session(data)

def end_session():
    data = load_session()
    data["status"] = "SSD"
    data["players"] = 0
    data["ip"] = "0.0.0.0"
    save_session(data)