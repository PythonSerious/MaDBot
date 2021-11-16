from discord import Client, Intents, Embed
from discord_slash import SlashCommand, SlashContext
from discord.ext.commands import Bot
import json


def prefix(new=False):
    if not new:
        with open("./config/generalConfiguration.json", "r") as rawFile:
            jsonfile = json.load(rawFile)
            return jsonfile["prefix"]

def devMode

bot = Bot(command_prefix=prefix())
slash = SlashCommand(bot)






