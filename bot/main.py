import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import threading

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

api = Flask(__name__)

# ------------------------
# STORE STATUS
# ------------------------
bot_status = {
    "text": "Nova Roleplay",
    "type": "playing"
}


# ------------------------
# DISCORD READY
# ------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await update_status()


async def update_status():
    text = bot_status["text"]
    status_type = bot_status["type"]

    activity = None

    if status_type == "playing":
        activity = discord.Game(name=text)
    elif status_type == "watching":
        activity = discord.Activity(type=discord.ActivityType.watching, name=text)
    elif status_type == "listening":
        activity = discord.Activity(type=discord.ActivityType.listening, name=text)

    await bot.change_presence(activity=activity)


# ------------------------
# COMMANDS
# ------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


# ------------------------
# API: SET STATUS
# ------------------------
@api.route("/set-status", methods=["POST"])
def set_status():
    global bot_status
    data = request.json

    bot_status = {
        "text": data.get("text", "Nova Roleplay"),
        "type": data.get("type", "playing")
    }

    return {"success": True}


# ------------------------
# API: PATROL MESSAGE
# ------------------------
@api.route("/patrol", methods=["POST"])
def patrol():
    data = request.json

    channel_id = int(data["channel_id"])
    channel = bot.get_channel(channel_id)

    if channel:
        embed = discord.Embed(
            title="🚓 Patrol Announcement",
            description=f"{data['date']} at {data['time']}",
            color=0x2b2d31
        )

        return {"success": True}

    return {"error": "Channel not found"}


# ------------------------
# RUN BOTH
# ------------------------
def run_api():
    api.run(host="0.0.0.0", port=5001)


threading.Thread(target=run_api).start()
bot.run(TOKEN)