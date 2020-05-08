import discord
import asyncio

cli = discord.Client()

@cli.event
async def on_ready():
    print("Hello there")

@cli.event
async def on_message(message):
    print("Bien reçu : <" + message.content + ">")
