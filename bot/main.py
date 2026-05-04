import discord
from discord.ext import commands
import asyncio
import json
import os
import threading
from flask import Flask, request, jsonify

# -------------------------
# ENV
# -------------------------
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "1451380734299345089"))

if not TOKEN:
    raise Exception("Missing DISCORD_TOKEN in Railway variables")

# -------------------------
# BOT SETUP
# -------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------
# FLASK API (FOR DASHBOARD)
# -------------------------
api = Flask(__name__)


# =========================
# STATUS GET
# =========================
@api.route("/status", methods=["GET"])
def status():
    return jsonify({
        "online": True,
        "bot": str(bot.user) if bot.user else "starting"
    })


# =========================
# STATUS SET
# =========================
@api.route("/status/set", methods=["POST"])
def set_status():
    data = request.json

    text = data.get("text", "Nova Roleplay")
    type_ = data.get("type", "playing")

    if type_ == "playing":
        activity = discord.Game(name=text)

    elif type_ == "watching":
        activity = discord.Activity(type=discord.ActivityType.watching, name=text)

    elif type_ == "listening":
        activity = discord.Activity(type=discord.ActivityType.listening, name=text)

    else:
        activity = discord.Game(name=text)

    asyncio.run_coroutine_threadsafe(
        bot.change_presence(activity=activity),
        bot.loop
    )

    return jsonify({"success": True})


# =========================
# SEND MESSAGE
# =========================
@api.route("/send", methods=["POST"])
def send_message():
    data = request.json

    channel = bot.get_channel(int(data["channel"]))
    message = data["message"]

    if not channel:
        return jsonify({"success": False})

    asyncio.run_coroutine_threadsafe(
        channel.send(message),
        bot.loop
    )

    return jsonify({"success": True})


# =========================
# PATROL CREATE
# =========================
@api.route("/patrol/create", methods=["POST"])
def patrol_create():
    data = request.json

    os.makedirs("data", exist_ok=True)

    with open("data/patrol_request.json", "w") as f:
        json.dump({
            "date": data["date"],
            "time": data["time"]
        }, f)

    return jsonify({"success": True})


# =========================
# BOT EVENTS
# =========================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")


# -------------------------
# RUN API SERVER
# -------------------------
def run_api():
    api.run(host="0.0.0.0", port=5001)


def start():
    threading.Thread(target=run_api).start()
    bot.run(TOKEN)


if __name__ == "__main__":
    start()