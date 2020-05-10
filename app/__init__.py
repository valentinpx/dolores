import discord
import asyncio
from config import cfg
from .controller import Controller
from discord.utils import get

cli = discord.Client()

@cli.event
async def on_ready():
    print("Hello there !")

@cli.event
async def on_message(message):
    if (message.author.id == cfg.id):
        return (0)
    controller = Controller(message.author.guild)
    channel = message.channel
    m_arr = message.content.split(" ")

    if ((m_arr[0].lower() == "dolores" or m_arr[0].lower() == "ds") and len(m_arr) > 2):
        if (m_arr[1] == "reu"):
            if (m_arr[2] == "add"):
                await channel.send(await controller.reu_add(m_arr[3]))
            if (m_arr[2] == "del"):
                await channel.send(await controller.reu_del(m_arr[3]))
            if (m_arr[2] == "invite"):
                await channel.send(await controller.reu_invite(m_arr[3], message.mentions))

@cli.event
async def on_reaction_add(reaction, user):
    controller = Controller(reaction.message.author.guild)
    message = reaction.message
    channel = message.channel
    title = channel.category.name

    if (user.id == cfg.id):
        return (0)

    if (message.content == cfg.command_message):
        for pinned in await channel.pins():
            if (str(reaction) != "🛎️" and (pinned.content.split(": ")[0] == cfg.reu_param_message.split(": ")[0] or pinned.content == cfg.reu_message)):
                return (0)

        if (str(reaction) == "💼"):
            await controller.reu_param(channel)
        if (str(reaction) == "🛎️"):
            await channel.send(await controller.reu_ping(title, user, channel))
        if (str(reaction) == "❌"):
            ret = await controller.reu_kick(user, title)
            if (ret != 0):
                await channel.send(ret)
        else:
            await message.remove_reaction(reaction, user)

    if (message.content.split(": ")[0] == cfg.reu_param_message.split(": ")[0]):
        if (str(reaction) == "⬅️" or str(reaction) == "➡️"):
            await controller.reu_time_set(message, str(reaction))
        if (str(reaction) == "✅"):
            await controller.reu_start(message)
        else:
            await message.remove_reaction(reaction, user)
    
    if (message.content == cfg.reu_message):
        if (str(reaction) == "⏱️"):
            await channel.send(await controller.reu_time_left(message))
        if (str(reaction) == "❌"):
            await channel.send(await controller.reu_end(message, True))
        else:
            await message.remove_reaction(reaction, user)
