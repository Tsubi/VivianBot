import discord
import os
import random

from keep_alive import keep_alive

client = discord.Client()

#Vivian Simple Information----------------------------------------------------
#Listen words
vivAttention = ["Vivian", "vivian", "virb", "birb", "Virb"]
vivCommands = ["!pet"]
#Responses
vivBirdNoises = ["Chirp!", "Cheep!", "Peep peep!", "Chirp chirp!", "Tweet tweet!"]

#start
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#listens for a message
@client.event
async def on_message(message):
    #makes sure that Vivian doesn't responde to her own messages
    if message.author == client.user:
        return

    #the message content variable
    msg = message.content

    #respond with a random string from the array
    if any(word in msg for word in vivAttention):
        await message.channel.send(random.choice(vivBirdNoises))

  #Commands---------------------------------------------------------------------
    #!pet
    if msg.startswith(vivCommands[0]):
        await message.channel.send(random.choice(vivBirdNoises) + " <:VivianPet:790248658054283274>")

#reaction add event
@client.event
async def on_raw_reaction_add(payload):
  msg_id = payload.message_id

  #Pronoun Roles
  if msg_id == 802997626995343370:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

    if payload.emoji.id == 802976289379713025:
      #He/Him
      role = discord.utils.get(guild.roles, id=802943259596685332)
    elif payload.emoji.id == 802976289597947914:
      #She/Her
      role = discord.utils.get(guild.roles, id=802943355960164372)
    elif payload.emoji.id == 802976289681834014:
      #They/Them
      role = discord.utils.get(guild.roles, id=802943394409480202)
    
    if role is not None:
      member = payload.member
      if member is not None:
        await member.add_roles(role)

  #Game Roles
  if msg_id == 802997668304650280:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

    if payload.emoji.id == 803000326184894496:
      #Art Games
      role = discord.utils.get(guild.roles, id=802943449404801054)
    elif payload.emoji.id == 803000326218317844:
      #OC Questions
      role = discord.utils.get(guild.roles, id=802943523979526174)
    elif payload.emoji.id == 978373881268146256:
      #Gamerz
      role = discord.utils.get(guild.roles, id=978375025461719070)
    
    if role is not None:
      member = payload.member
      print(member.name + '1')
      if member is not None:
        await member.add_roles(role)
        print(member.name + '2')

  #Stream Roles
  if msg_id == 931991719136878602:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

    if payload.emoji.id == 845447895758274631:
      #Stream notification
      role = discord.utils.get(guild.roles, id=932759248755126303)
    
    if role is not None:
      member = payload.member
      print(member.name + '1')
      if member is not None:
        await member.add_roles(role)
        print(member.name + '2')

#reaction remove event
@client.event
async def on_raw_reaction_remove(payload):
  msg_id = payload.message_id

  #Pronoun Roles
  if msg_id == 802997626995343370:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

    if payload.emoji.id == 802976289379713025:
      #He/Him
      role = discord.utils.get(guild.roles, id=802943259596685332)
      print(role.name)
    elif payload.emoji.id == 802976289597947914:
      #She/Her
      role = discord.utils.get(guild.roles, id=802943355960164372)
      print(role.name)
    elif payload.emoji.id == 802976289681834014:
      #They/Them
      role = discord.utils.get(guild.roles, id=802943394409480202)
      print(role.name)
    
    if role is not None:
      member = await guild.fetch_member(payload.user_id)
      print(member.name + '1')
      if member is not None:
        await member.remove_roles(role)
        print(member.name + '2')

  #Game Roles
  if msg_id == 802997668304650280:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

    if payload.emoji.id == 803000326184894496:
      #Art Games
      role = discord.utils.get(guild.roles, id=802943449404801054)
    elif payload.emoji.id == 803000326218317844:
      #OC Questions
      role = discord.utils.get(guild.roles, id=802943523979526174)
    elif payload.emoji.id == 978373881268146256:
      #Gamerz
      role = discord.utils.get(guild.roles, id=978375025461719070)
    
    if role is not None:
      member = await guild.fetch_member(payload.user_id)
      if member is not None:
        await member.remove_roles(role)

  #Stream Roles
  if msg_id == 931991719136878602:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

    if payload.emoji.id == 845447895758274631:
      #Stream notification
      role = discord.utils.get(guild.roles, id=932759248755126303)
    
    if role is not None:
      member = await guild.fetch_member(payload.user_id)
      if member is not None:
        await member.remove_roles(role)

keep_alive()

client.run(os.getenv('TOKEN'))