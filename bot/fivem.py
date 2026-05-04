import requests

def get_player_count(ip):
    try:
        res = requests.get(f"http://{ip}/players.json", timeout=5)
        return len(res.json())
    except:
        return 0