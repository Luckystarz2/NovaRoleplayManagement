import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
import threading
from flask import Flask, request, jsonify

# ------------------------
# ENV
# ------------------------
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------
# STATUS STORAGE
# ------------------------
bot_status = {
    "text": "Nova Roleplay",
    "type": "playing"
}

# ------------------------
# FLASK API
# ------------------------
api = Flask(__name__)

# ------------------------
# UPDATE STATUS
# ------------------------
async def update_status():
    text = bot_status["text"]
    status_type = bot_status["type"]

    if status_type == "playing":
        activity = discord.Game(name=text)
    elif status_type == "watching":
        activity = discord.Activity(type=discord.ActivityType.watching, name=text)
    elif status_type == "listening":
        activity = discord.Activity(type=discord.ActivityType.listening, name=text)
    else:
        activity = discord.Game(name=text)

    await bot.change_presence(activity=activity)

# ------------------------
# READY EVENT
# ------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Sync error: {e}")

    await update_status()

# ------------------------
# PREFIX COMMAND
# ------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# ------------------------
# SLASH COMMAND: PING
# ------------------------
@bot.tree.command(name="ping", description="Ping bot")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)

# ------------------------
# SLASH COMMAND: PATROL
# ------------------------
@bot.tree.command(name="patrolannounce", description="Send patrol announcement")
async def patrol(interaction: discord.Interaction, date: str, time: str):

    await interaction.response.defer()

    embed = discord.Embed(
        title="🚓 Patrol Announcement",
        description=f"📅 {date} at {time}\n\n✅ Yes\n🟠 Maybe\n❌ No",
        color=0x2b2d31
    )

    msg = await interaction.channel.send(embed=embed)

    await msg.add_reaction("✅")
    await msg.add_reaction("🟠")
    await msg.add_reaction("❌")

    await interaction.followup.send("Sent!", ephemeral=True)

# ======================================================
# 🔥 DASHBOARD API: SET STATUS
# ======================================================
@api.route("/set-status", methods=["POST"])
def set_status():
    global bot_status

    data = request.json

    bot_status = {
        "text": data.get("text", "Nova Roleplay"),
        "type": data.get("type", "playing")
    }

    asyncio.run_coroutine_threadsafe(update_status(), bot.loop)

    return jsonify({"success": True})

# ======================================================
# 🚓 DASHBOARD API: PATROL
# ======================================================
@api.route("/patrol", methods=["POST"])
def patrol_api():
    data = request.json

    async def send():
        try:
            channel = await bot.fetch_channel(int(data["channel_id"]))

            embed = discord.Embed(
                title="🚓 Patrol Announcement",
                description=f"📅 {data['date']} at {data['time']}\n\n"
                            "✅ Yes\n🟠 Maybe\n❌ No",
                color=0x2b2d31
            )

            msg = await channel.send(embed=embed)

            await msg.add_reaction("✅")
            await msg.add_reaction("🟠")
            await msg.add_reaction("❌")

        except Exception as e:
            print("Patrol API error:", e)

    asyncio.run_coroutine_threadsafe(send(), bot.loop)

    return jsonify({"success": True})

# ======================================================
# 💬 DASHBOARD API: SEND MESSAGE (THIS WAS MISSING)
# ======================================================
@api.route("/send", methods=["POST"])
def send_message():
    data = request.json

    async def send():
        try:
            channel = await bot.fetch_channel(int(data["channel"]))
            await channel.send(data["message"])
        except Exception as e:
            print("Send API error:", e)

    asyncio.run_coroutine_threadsafe(send(), bot.loop)

    return jsonify({"success": True})

# ------------------------
# RUN FLASK API THREAD
# ------------------------
def run_api():
    api.run(host="0.0.0.0", port=5001)

threading.Thread(target=run_api, daemon=True).start()

# ------------------------
# RUN BOT
# ------------------------
bot.run(TOKEN)