import os
from core import discord

DISCORD_API_KEY = os.getenv("DISCORD_BOT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    discord.run(discord_api_key=DISCORD_API_KEY, openai_api_key=OPENAI_API_KEY)
