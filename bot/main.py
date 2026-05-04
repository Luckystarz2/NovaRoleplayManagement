import discord
from discord.ext import commands
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1451380734299345089

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# -------------------------
# PATROL WATCHER
# -------------------------
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
                            "✅ If you can attend\n"
                            "🟠 If unsure\n"
                            "❌ If you can't attend"
                        ),
                        color=0x2b2d31
                    )

                    msg = await channel.send(embed=embed)

                    await msg.add_reaction("✅")
                    await msg.add_reaction("🟠")
                    await msg.add_reaction("❌")

                os.remove(path)

            except Exception as e:
                print("Error:", e)

        await asyncio.sleep(5)


# -------------------------
# READY EVENT
# -------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(patrol_watcher())


# -------------------------
# TEST COMMAND
# -------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")


bot.run(TOKEN)