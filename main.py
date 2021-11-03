import os
import discord
import re
from roller import Roller
import random
from datetime import datetime


PREFIX = "::"               # The prefix used for commands
client = discord.Client()   # The bot client
roller = Roller()           # The roller
timeout_zone = {}           # Bruh chill
boneless = [
    "b̵͚̙̱̱͈͇̜̪̯̈̅͊́̈́̚͘o̵̟̖̮̞̖̅̚n̷̟͖̮̼̪̆̒̆͜ȩ̶̧̛̫̰͔̼̭̘̟͛̓̍͌ļ̷̞̣͎͊e̴̠̦̙̼̖̥̠͎̿̂̈́͗ͅs̶̭̝͉̺͍͍̹̬̗͊ͅs̸̢̢̙͎̹͔͕͎̭̣̅̅̈́",
    "ꙅꙅɘ|ɘᴎod",
    "ⓑⓞⓝⓔⓛⓔⓢⓢ",
    "ᗷᗝᑎᗴᒪᗴᔕᔕ",
    "🅱🅾🅽🅴🅻🅴🆂🆂",
    "БФИΞLΞSS",
    "𝚋̷𝚘̷𝚗̷𝚎̷𝚕̷𝚎̷𝚜̷𝚜̷",
    "๒๏ภєɭєรร",
    "Ⴆσɳҽʅҽʂʂ",
    "ɮօռɛʟɛֆֆ",
    "ᏰᎧᏁᏋᏝᏋᏕᏕ",
    "ცơŋɛƖɛʂʂ",
    "๖໐ຖēlēŞŞ",
    "ზσɳҽʅҽʂʂ",
    "βŐŃĔĹĔŚŚ",
    "ϦØЛƐŁƐらら",
    "ƁƠƝЄԼЄƧƧ",
    "ՅԾՌȝʅȝՏՏ"
]


@client.event
async def on_message(message):
    """
    Handle messages to initialize the roller

    message - the message that was sent
    """

    # Convert message to lower case and strip whitespace
    msg = message.content.lower()
    command = re.sub("\\s+", "", msg)

    if command == PREFIX + "roll":
        # Main command to start the roller
        await roller.start_roll(message.channel)
    elif command == PREFIX + "ping":
        # Ping command to check if the bot is still alive
        await message.channel.send("Pong!")
    elif client.user.id != message.author.id and \
            (msg.startswith("shoutout to") or msg.startswith("shout out to")):
        # Ok so these dudes need to chill out
        # This is a really quick and dirty way to limit shouting out to every
        # 2 minutes. Will something not work correctly? Probably. Is there a
        # better way to do it? Probably. But what's the worst that can happen?
        now = datetime.now().timestamp()
        if client.user.id in timeout_zone:
            timestamp = timeout_zone[client.user.id]
            if now - timestamp < 120:
                return

        # SHOUT OUT TO SHOUTING OUT
        timeout_zone[client.user.id] = now
        await message.channel.send(msg.upper())
    elif client.user.id != message.author.id and "pizza" in msg:
        # It better be boneless
        index = random.randint(0, len(boneless) - 1)
        await message.channel.send("That pizza better be " + boneless[index])


@client.event
async def on_raw_reaction_add(payload):
    """
    Handle when a reaction is added to roll the dice

    payload - the event payload
    """

    # Don't react to our own reactions
    if client.user.id != payload.user_id:
        user = await client.fetch_user(payload.user_id)
        await roller.roll(payload, user)


@client.event
async def on_raw_reaction_remove(payload):
    """
    Treat removes like adds so users can click the reaction multiple times to
    roll again

    payload - the event payload
    """

    # Don't have to worry about checking the user since the bot won't remove
    # reactions
    user = await client.fetch_user(payload.user_id)
    await roller.roll(payload, user)


@client.event
async def on_ready():
    """
    Handle when the bot has started
    """

    print(f'{client.user} has connected to Discord!')
    game = discord.Game("::roll")
    await client.change_presence(activity=game)


if __name__ == "__main__":
    """
    Startup
    """

    TOKEN = os.getenv("ROLL_WITH_LUCKY_TOKEN")
    client.run(TOKEN)
