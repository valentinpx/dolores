import discord
import asyncio
from discord.utils import get
from config import cfg

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
        command_channel = await category.create_text_channel("Commandes")
        await category.create_text_channel(name=title + " vocal")
        await category.create_voice_channel(name=title + " chat")
        message = await command_channel.send(cfg.command_message)
        await message.add_reaction(emoji="💼")
        await message.add_reaction(emoji="🛎️")
        await message.add_reaction(emoji="❌")
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
    
    async def reu_invite(self, title, users):
        if (get(self.server.roles, name=title) == None or get(self.server.categories, name=title) == None):
            return ("Impossible d'inviter l'utilisateur: titre introuvable")
        
        role = get(self.server.roles, name=title)
        
        for user in users:
            await user.add_roles(role)
        return ("Utilisateur(s) invité(s) !")
    
    async def reu_kick(self, author, title):
        role = get(self.server.roles, name=title)

        await asyncio.wait_for(author.remove_roles(role), timeout=1.0)
        if (len(role.members) == 0):
            await self.reu_del(title)
            return (0)
        return ("Utilisateur supprimé.")
