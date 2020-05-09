import discord
import asyncio
from discord.utils import get

class Controller():
    def __init__(self, server):
        self.server = server

    async def reu_add(self, title):
        if (get(self.server.roles, name=title) != None or get(self.server.categories, name=title) != None):
            return ("Impossible de créer la réunion: titre déjà utilisé")

        role = await self.server.create_role(name=title)
        category = await self.server.create_category(name=title)

        await category.set_permissions(self.server.default_role, view_channel=False)
        await category.set_permissions(role, view_channel=True)
        await category.create_text_channel(name=title + " vocal")
        await category.create_voice_channel(name=title + " chat")
        return ("Réunion créée !")

    async def reu_del(self, title):
        if (get(self.server.roles, name=title) == None or get(self.server.categories, name=title) == None):
            return ("Impossible de supprimer la réunion: titre introuvable")

        role = get(self.server.roles, name=title)
        category = get(self.server.categories, name=title)

        await role.delete()
        for channel in category.text_channels:
            await channel.delete()
        for channel in category.voice_channels:
            await channel.delete()
        await category.delete()
        return ("Réunion supprimée.")