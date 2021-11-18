from discord import Client, Intents, Embed
from discord_slash import SlashCommand, SlashContext, utils, ComponentContext
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, \
    wait_for_component, create_button
from discord_slash.model import ButtonStyle
from discord.ext.commands import Bot
import json
import re

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


bot = Bot(command_prefix=prefix(), Intents=Intents.all())
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True, override_type=False)

async def validator(ctx, list, objectName, object, msg, questionEmbed, inptype, comps=None):
    buttons = [
        create_button(style=ButtonStyle.green, label="Yes"),
        create_button(style=ButtonStyle.red, label="No")
    ]
    action_row = create_actionrow(*buttons)
    embed = Embed(title=f"{list}:", description=f"> Is the {objectName} correct?\n\n> ```{object.content}```",
                  color=0x2f3136)
    embed.set_author(
        icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
        name="Bug report system")
    await msg.edit(embed=embed, components=[action_row])

    def componentCheck(interaction):  # interaction is a ComponentContext type
        return ctx.author.id == interaction.author.id
    try:
        button_ctx: ComponentContext = await wait_for_component(bot, components=action_row, check=componentCheck,
                                                            timeout=25)
    except:
        embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
        embed.set_author(
            icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
            name="Bug report system")
        await msg.edit(embed=embed, components=[])
        return [False, 0]
    label = button_ctx.component["label"]
    if label == "Yes":
        return [True, object.content]
    else:
        if inptype == "message":
            await msg.edit(embed=questionEmbed, components=[])

            def check(m):
                return ctx.channel.id == m.channel.id and m.author.id == ctx.author.id
            try:
                response = await bot.wait_for('message', check=check, timeout=500)
            except:
                embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
                embed.set_author(
                    icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
                    name="Bug report system")
                await msg.edit(embed=embed, components=[])
                return [False, 0]
            await response.delete()
            await validator(button_ctx, list, objectName, response, msg, questionEmbed, inptype)


async def imageValidator(ctx, msg, response, questionEmbed, list):
    buttons = [
        create_button(style=ButtonStyle.green, label="Yes"),
        create_button(style=ButtonStyle.red, label="No")
    ]
    action_row = create_actionrow(*buttons)

    if response.attachments:
        url = response.attachments[0].url
    elif not response.attachments:
        if "http" in response.content and "://" in response.content:
            bannedextensions = ["com", "bat", "py", "cs", "c", "cpp", "js", "jar", "exe"]
            url = response.content
            for entry in bannedextensions:
                if f".{entry}" in url:
                    desc = questionEmbed.description
                    newdesc = f"**🚫 Dis-allowed file extension!**\n\n{desc}"
                    questionEmbed.description = newdesc
                    await msg.edit(embed=questionEmbed, components=[])

                    def check(m):
                        return ctx.channel.id == m.channel.id and m.author.id == ctx.author.id

                    try:
                        response = await bot.wait_for('message', check=check, timeout=500)
                    except:
                        embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
                        embed.set_author(
                            icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
                            name="Bug report system")
                        await msg.edit(embed=embed, components=[])
                        return [False, 0]
                    await response.delete()
                    questionEmbed.description = desc
                    return await imageValidator(ctx, msg, response, questionEmbed, list)


        else:

            desc = questionEmbed.description
            newdesc = f"**⚠️ Invalid URL!**\n\n{desc}"
            questionEmbed.description = newdesc
            await msg.edit(embed=questionEmbed, components=[])

            def check(m):
                return ctx.channel.id == m.channel.id and m.author.id == ctx.author.id

            try:
                response = await bot.wait_for('message', check=check, timeout=500)
            except:
                embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
                embed.set_author(
                    icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
                    name="Bug report system")
                await msg.edit(embed=embed, components=[])
                return [False, 0]
            await response.delete()
            questionEmbed.description = desc
            return await imageValidator(ctx, msg, response, questionEmbed, list)
    embed = Embed(title=f"{list}:", description=f"> Is the [attachment]({url}) correct?\n", color=0x2f3136)
    embed.set_image(url=url)
    embed.set_author(
        icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
        name="Bug report system")
    await msg.edit(embed=embed, components=[action_row])

    def componentCheck(interaction):  # interaction is a ComponentContext type
        return ctx.author.id == interaction.author.id
    try:
        button_ctx: ComponentContext = await wait_for_component(bot, components=action_row, check=componentCheck,
                                                            timeout=25)
    except:
        embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
        embed.set_author(
            icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
            name="Bug report system")
        await msg.edit(embed=embed, components=[])
        return [False, 0]
    label = button_ctx.component["label"]
    if label == "Yes":
        return [True, url]
    else:
        await msg.edit(embed=questionEmbed, components=[])

        def check(m):
            return ctx.channel.id == m.channel.id and m.author.id == ctx.author.id

        try:
            response = await bot.wait_for('message', check=check, timeout=500)
        except:
            embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
            embed.set_author(
                icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
                name="Bug report system")
            await msg.edit(embed=embed, components=[])
            return [False, 0]
        await response.delete()
        return await imageValidator(button_ctx, msg, response, questionEmbed, list)


@slash.slash(name="create")
async def _create(ctx: SlashContext):
    embed = Embed(title="Select Board:", description="> Select a list you would like to submit to.", color=0x2f3136)
    embed.set_author(
        icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
        name="Bug report system")
    select = create_select(
        options=[
            create_select_option("Building Bugs", description="List ID: {}", value="bb", emoji="1️⃣"),
            create_select_option("Script Bugs", description="List ID: {}", value="sb", emoji="2️⃣"),
            create_select_option("Other Bugs", description="List ID: {}", value="ob", emoji="3️⃣"),
        ],
        placeholder="Choose a list below.",
        min_values=1,
        max_values=1
    )
    action_row = create_actionrow(select)
    msg = await ctx.send(embed=embed, hidden=False, components=[action_row])

    def componentCheck(interaction):  # interaction is a ComponentContext type
        return ctx.author.id == interaction.author.id
    try:
        button_ctx: ComponentContext = await wait_for_component(bot, components=action_row, check=componentCheck,
                                                            timeout=25)
    except:
        embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
        embed.set_author(
            icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
            name="Bug report system")
        await msg.edit(embed=embed, components=[])
    for entry in button_ctx.component['options']:
        if entry['value'] == button_ctx.selected_options[0]:
            list = entry['label']
            break

    embed = Embed(title=f"{list}:", description="> What's the report title?", color=0x2f3136)
    embed.set_author(
        icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
        name="Bug report system")
    await msg.edit(embed=embed, components=[])

    def check(m):
        return ctx.channel.id == m.channel.id and m.author.id == ctx.author.id
    try:
        response = await bot.wait_for('message', check=check, timeout=500)
    except:
        embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
        embed.set_author(
            icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
            name="Bug report system")
        await msg.edit(embed=embed, components=[])
        return [False, 0]
    await response.delete()
    validatedResponse = await validator(button_ctx, "Building Bugs", "title", response, msg, embed, "message")
    title = validatedResponse[1]
    if validatedResponse[0]:
        embed = Embed(title=f"{list}:", description="> What's the report description?", color=0x2f3136)
        embed.set_author(
            icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
            name="Bug report system")
        await msg.edit(embed=embed, components=[])

        def check(m):
            return ctx.channel.id == m.channel.id and m.author.id == ctx.author.id
        try:
            response = await bot.wait_for('message', check=check, timeout=500)
        except:
            embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
            embed.set_author(
                icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
                name="Bug report system")
            await msg.edit(embed=embed, components=[])
            return [False, 0]
        await response.delete()
        validatedResponse = await validator(button_ctx, "Building Bugs", "description", response, msg, embed, "message")
        descr = validatedResponse[1]
        if validatedResponse:
            embed = Embed(title=f"{list}:", description="> Attach evidence below. (url or uploaded file)",
                          color=0x2f3136)
            embed.set_author(
                icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
                name="Bug report system")
            await msg.edit(embed=embed, components=[])

            def check(m):
                return ctx.channel.id == m.channel.id and m.author.id == ctx.author.id
            try:
                response = await bot.wait_for('message', check=check, timeout=500)
            except:
                embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
                embed.set_author(
                    icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
                    name="Bug report system")
                await msg.edit(embed=embed, components=[])
                return [False, 0]
            await response.delete()
            validatedResponse = await imageValidator(button_ctx, msg, response, embed, list)
            link = validatedResponse[1]
            if validatedResponse:
                if list == "Script Bugs":
                    color = 0xc773df
                elif list == "Building Bugs":
                    color = 0x1c76bf
                else:
                    color = 0xf5f5f5
                embed = Embed(color=color, title=title, description=f"**Description**\n> {descr}\n\n**Attachment**")
                embed.set_image(url=link)
                embed.set_author(
                    icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
                    name="Bug report [CARD PREVIEW]")
                buttons = [
                    create_button(style=ButtonStyle.green, label="Yes"),
                    create_button(style=ButtonStyle.red, label="No (Cancel Progress)")
                ]
                action_row = create_actionrow(*buttons)

                if response.attachments:
                    url = response.attachments[0].url
                elif not response.attachments:
                    url = response

                await msg.edit(embed=embed, components=[action_row])

                def componentCheck(interaction):  # interaction is a ComponentContext type
                    return ctx.author.id == interaction.author.id
                try:
                    button_ctx: ComponentContext = await wait_for_component(bot, components=action_row,
                                                                        check=componentCheck, timeout=25)
                except:
                    embed = Embed(description=f"> **The timeout has been reached.**\n", color=0x2f3136)
                    embed.set_author(
                        icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
                        name="Bug report system")
                    await msg.edit(embed=embed, components=[])
                label = button_ctx.component["label"]
                if label == "Yes":
                    await ctx.send("Do wizardly trello post shit here.")
                else:
                    embed = Embed(title=f"{list}:", description="> Card Canceled.", color=0x2f3136)
                    embed.set_author(
                        icon_url="https://cdn.discordapp.com/icons/638963040691290114/b4e6d524951945366ab6d68fbe85523e.png?size=4096",
                        name="Bug report system")
                    await msg.edit(embed=embed, components=[])


bot.run(token(), bot=True)
