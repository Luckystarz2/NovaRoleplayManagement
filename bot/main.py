import discord
from discord.ext import commands
import asyncio
import json
import os
import threading
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# -------------------------
# LOAD ENV (LOCAL + RAILWAY SAFE)
# -------------------------
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "1451380734299345089"))

if not TOKEN:
    raise Exception("DISCORD_TOKEN is missing. Set it in Railway Variables.")

# -------------------------
# DISCORD BOT SETUP
# -------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

BOT_INSTANCE = None

# -------------------------
# FLASK API (BOT CONTROL BRIDGE)
# -------------------------
api = Flask(__name__)


# =========================
# STATUS CONTROL
# =========================
@api.route("/status/set", methods=["POST"])
def set_status():
    data = request.json

    status_type = data.get("type", "playing")
    text = data.get("text", "Nova Roleplay")

    activity = None

    if status_type == "playing":
        activity = discord.Game(name=text)

    elif status_type == "watching":
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=text
        )

    elif status_type == "listening":
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name=text
        )

    elif status_type == "competing":
        activity = discord.Activity(
            type=discord.ActivityType.competing,
            name=text
        )

    if activity:
        asyncio.run_coroutine_threadsafe(
            bot.change_presence(activity=activity),
            bot.loop
        )

    return jsonify({"success": True})


# =========================
# BOT STATUS CHECK
# =========================
@api.route("/status", methods=["GET"])
def status():
    return jsonify({
        "online": True,
        "bot": str(bot.user) if bot.user else "starting"
    })


# =========================
# BOT RESTART (RAILWAY SAFE)
# =========================
@api.route("/restart", methods=["POST"])
def restart():
    os._exit(0)


# =========================
# PATROL WATCHER
# =========================
async def patrol_watcher():
    await bot.wait_until_ready()

    path = "data/patrol_request.json"

    while not bot.is_closed():

        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)

                channel = bot.get_channel(CHANNEL_ID)

                if channel:
                    embed = discord.Embed(
                        title="🚓 Patrol Announcement",
                        description=(
                            f"📅 **{data['date']} at {data['time']}**\n\n"
                            "✅ Attending\n"
                            "🟠 Unsure\n"
                            "❌ Not attending"
                        ),
                        color=0x2b2d31
                    )

                    msg = await channel.send(embed=embed)

                    await msg.add_reaction("✅")
                    await msg.add_reaction("🟠")
                    await msg.add_reaction("❌")

                os.remove(path)

            except Exception as e:
                print("Patrol error:", e)

        await asyncio.sleep(5)


# =========================
# EVENTS
# =========================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    bot.loop.create_task(patrol_watcher())


# =========================
# COMMANDS
# =========================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")


# =========================
# RUN API SERVER
# =========================
def run_api():
    api.run(host="0.0.0.0", port=5001)


# =========================
# START EVERYTHING
# =========================
def start():
    global BOT_INSTANCE
    BOT_INSTANCE = bot

    threading.Thread(target=run_api).start()

    bot.run(TOKEN)


if __name__ == "__main__":
    start()