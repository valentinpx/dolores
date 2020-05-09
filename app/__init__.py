import discord
import asyncio
from .controller import Controller
from discord.utils import get

cli = discord.Client()

@cli.event
async def on_ready():
    print("Hello there !")

@cli.event
async def on_message(message):
    controller = Controller(message.author.guild)
    m_arr = message.content.split(" ")

    if ((m_arr[0].lower() == "dolores" or m_arr[0].lower() == "ds") and len(m_arr) > 2):
        if (m_arr[1] == "reu"):
            if (m_arr[2] == "add"):
                await controller.reu_add(m_arr[3])
            if (m_arr[2] == "del"):
                await controller.reu_del(m_arr[3])
