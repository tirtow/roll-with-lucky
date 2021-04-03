import os
import discord
from dotenv import load_dotenv
import re


PREFIX = "::"   # The prefix used for commands
client = discord.Client()


@client.event
async def on_message(message):
    """
    """

    # Convert message to lower case and strip whitespace
    command = message.content.lower()
    command = re.sub("\\s+", "", command)

    if command == PREFIX + "ping":
        # Ping command to check if the bot is still alive
        await message.channel.send("Pong!")


@client.event
async def on_ready():
    """
    Handle when the bot has started
    """

    print(f'{client.user} has connected to Discord!')


if __name__ == "__main__":
    """
    Startup
    """

    load_dotenv()
    TOKEN = os.getenv("ROLL_WITH_LUCKY_TOKEN")
    client.run(TOKEN)
