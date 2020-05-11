import discord
import asyncio
import datetime
from discord.utils import get
from config import cfg

class Controller():
    def __init__(self, server):
        self.server = server

    async def reu_add(self, title):
        if (get(self.server.roles, name=title) != None or get(self.server.categories, name=title) != None):
            return ("Impossible de créer la réunion: titre déjà utilisé")
        if (" - " in title):
            return ("Impossible de créer la réunion: le titre ne peutt pas contenir \" - \"")

        role = await self.server.create_role(name=title)
        category = await self.server.create_category(name=title)

        await category.set_permissions(self.server.default_role, view_channel=False)
        await category.set_permissions(role, view_channel=True)
        command_channel = await category.create_text_channel("Commandes")
        await category.create_text_channel(name=title + " chat")
        await category.create_voice_channel(name=title + " vocal")
        message = await command_channel.send(cfg.command_message)
        await message.pin()
        await message.add_reaction(emoji="💼")
        await message.add_reaction(emoji="🛎️")
        await message.add_reaction(emoji="❌")
        await command_channel.set_permissions(self.server.default_role, send_messages=False, view_channel=False)
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
    
    async def reu_ping(self, title, author, channel):
        role = get(self.server.roles, name=title)
        mention = "https://discordapp.com/channels/"+ str(self.server.id) +"/" + str(channel.id)

        for member in role.members:
            if (member != author):
                channel = await member.create_dm()
                await channel.send("Hey ! On a besoin de vous dans la réunion " + title + ".\n La réunion en question: " + mention)
        return ("Utilisateur(s) notifié(s) !")
    
    async def reu_param(self, channel):
        message = await channel.send(cfg.reu_param_message)

        await message.pin()
        await message.add_reaction(emoji="⬅️")
        await message.add_reaction(emoji="✅")
        await message.add_reaction(emoji="➡️")

    async def reu_time_set(self, message, emoji):
        content_arr = message.content.split(": ")
        hours = int(content_arr[1]) + (1 if (emoji == "➡️") else -1)

        if (hours > 0):
            await message.edit(content=(content_arr[0] + ": " + str(hours)))
        else:
            await message.channel.send("Erreur: la réunion doit durer au moins une heure !")

    async def reu_start(self, param_message):
        channel = param_message.channel
        category = get(self.server.categories, id=channel.category_id)
        hours = int(param_message.content.split(": ")[1])

        await category.edit(name=category.name + " - réunion de " + str(hours) + "h")
        await param_message.delete()
        message = await channel.send(cfg.reu_message)
        await message.pin()
        await message.add_reaction(emoji="❌")
        await message.add_reaction(emoji="⏱️")
        print("Réunion commencée, attente de : " + str(hours) + "h")
        await asyncio.sleep(hours * 60 * 60)
        print("Réunion terminée !")
        await self.reu_end(message, False)
    
    async def reu_end(self, message, canceled):
        category = get(self.server.categories, id=message.channel.category_id)

        await message.delete()
        await category.edit(name=category.name.split(" - ")[0])
        if (canceled == True):
            return ("Réunion annulée.")
        return ("Réunion terminée !")
    
    async def reu_time_left(self, message):
        category = get(self.server.categories, id=message.channel.category_id)
        duration = datetime.timedelta(hours=int(category.name.split(" - réunion de ")[1][:1]))
        goal = message.created_at + duration
        now = datetime.datetime.utcnow()
        left = str(goal - now).split(":")

        return ("Temps restant: " + left[0] + ":" + left[1])
