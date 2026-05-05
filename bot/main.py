import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

# ------------------------
# ENV
# ------------------------
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ DISCORD_TOKEN is missing!")

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
CORS(api)  # 🔥 FIX CORS (IMPORTANT)

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
# COMMANDS
# ------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.tree.command(name="ping")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)

@bot.tree.command(name="patrolannounce")
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

# ------------------------
# API: STATUS
# ------------------------
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

# ------------------------
# API: PATROL
# ------------------------
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
            print("Patrol error:", e)

    asyncio.run_coroutine_threadsafe(send(), bot.loop)

    return jsonify({"success": True})

# ------------------------
# API: SEND MESSAGE
# ------------------------
@api.route("/send", methods=["POST"])
def send_message():
    data = request.json

    async def send():
        try:
            channel = await bot.fetch_channel(int(data["channel"]))
            await channel.send(data["message"])
        except Exception as e:
            print("Send error:", e)

    asyncio.run_coroutine_threadsafe(send(), bot.loop)

    return jsonify({"success": True})

# ------------------------
# RUN FLASK THREAD
# ------------------------
def run_api():
    api.run(host="0.0.0.0", port=5001)

threading.Thread(target=run_api, daemon=True).start()

# ------------------------
# RUN BOT
# ------------------------
bot.run(TOKEN)