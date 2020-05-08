#!/usr/bin/env python3

import discord
import asyncio

cli = discord.Client()

@cli.event
async def on_ready():
    print("Hello there")

@cli.event
async def on_message(message):
    print("Bien reçu : <" + message.content + ">")

cli.run("NzA4MzgyNTg4ODU0ODYxODc2.XrWovA.n-oNIOKqkQKA8qpPnDNOnR6sx4Q")