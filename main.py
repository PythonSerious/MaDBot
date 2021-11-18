from discord import Client, Intents, Embed
from discord_slash import SlashCommand, SlashContext
from discord.ext.commands import Bot
import json

def token():
    with open("./config/generalConfiguration.json", "r") as rawFile:
        jsonfile = json.load(rawFile)
        return jsonfile["token"]


def prefix(new=False):
    if not new:
        with open("./config/generalConfiguration.json", "r") as rawFile:
            jsonfile = json.load(rawFile)
            return jsonfile["prefix"]

def devMode(toggle=False):
    with open("./config/generalConfiguration.json", "r") as rawFile:
        jsonfile = json.load(rawFile)
        if not toggle:
            return jsonfile["devMode"]
        with open("./config/generalConfiguration.json", "w") as f:
            jsonfile["devMode"] = not jsonfile["devMode"]
            json.dump(jsonfile, f, indent=4)
            return jsonfile["devMode"]


bot = Bot(command_prefix=prefix())
slash = SlashCommand(bot)

@slash.slash(name="create")
async def _create(ctx: SlashContext):
    embed = Embed(title="Empheral Message")
    await ctx.send(embed=embed, hidden=True)


bot.run(token(), bot=True)