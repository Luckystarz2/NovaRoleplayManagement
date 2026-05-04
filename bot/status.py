import discord
import json
from bot.config import STATUS_CHANNEL_ID

SESSION_FILE = "data/session.json"
MESSAGE_FILE = "data/status_message.txt"

def load_session():
    with open(SESSION_FILE, "r") as f:
        return json.load(f)

def load_message_id():
    try:
        with open(MESSAGE_FILE, "r") as f:
            return int(f.read())
    except:
        return None

def save_message_id(msg_id):
    with open(MESSAGE_FILE, "w") as f:
        f.write(str(msg_id))


async def update_status(bot):
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    data = load_session()

    embed = discord.Embed(
        title="Nova Roleplay Status",
        color=0x00ff00 if data["status"] == "SSU" else 0xff0000
    )

    embed.add_field(name="Status", value=data["status"], inline=False)
    embed.add_field(name="Players", value=data["players"], inline=True)
    embed.add_field(name="IP", value=data["ip"], inline=True)

    msg_id = load_message_id()

    if msg_id is None:
        msg = await channel.send(embed=embed)
        save_message_id(msg.id)
    else:
        try:
            msg = await channel.fetch_message(msg_id)
            await msg.edit(embed=embed)
        except:
            msg = await channel.send(embed=embed)
            save_message_id(msg.id)