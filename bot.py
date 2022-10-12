import discord
import os
import random
import logging
import glob
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv

log = logging.getLogger('VivianBot')

console_handler = StreamHandler()
console_handler.setLevel(logging.WARNING)

file_handler = TimedRotatingFileHandler('vivian.log', when='D', interval=1, backupCount=7)
file_handler.setLevel(logging.INFO)

log.addHandler(console_handler)
log.addHandler(file_handler)

#Loading .env file, contains sensitive client information
load_dotenv()

client = discord.Client(intents=discord.Intents.all())
guild_id = 580495406534885385 # Vivian's Birdhouse
guild = None # not populated until bot is started

#Vivian Simple Information----------------------------------------------------
#Listen words
vivAttention = ["vivian", "virb", "birb"]

vivGlobalCommands = ["!pet"]

mod_id = 580496944686694407
mod_role = None # not populated until bot is started
vivModCommands = ["!raffle", "!endraffle"]


# Pet Responses
vivBirdNoises = ["Chirp!", "Cheep!", "Peep peep!", "Chirp chirp!", "Tweet tweet!"]
# Active raffles. Stored as a list of user ids.
raffles = {}
for file in glob.glob("*.raffle"):
  raffle_name = os.path.splitext(file)[0]
  raffle_entrants = []
  with open(file) as f:
    raffle_entrants = f.read().split()
  raffles[raffle_name] = raffle_entrants

    

#start
@client.event
async def on_ready():
    global guild, mod_role
    log.info(f'Bot logged in as: {client.user}')
    guild = client.get_guild(guild_id)
    mod_role = guild.get_role(mod_id) 

#listens for a message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    
    # get information about who sent the message
    author = message.author

    # where the message was sent
    channel = message.channel

    #the message content variable, string representation
    content = message.content
    # for easy use in string matching
    content_lower = content_lower.lower()
    # for easy use checking against commands
    command = content_lower.split()[0]

    log.debug(
      f"""Parsing a message: 
        Author: {author.name}
        Channel: {channel.name}
        Content: {content}"""
    )

    # Global User Commands---------------------------------------------------------------------
    if command in vivGlobalCommands:
      #!pet
      if content_lower.startswith(vivGlobalCommands[0]):
          await message.channel.send(f"{random.choice(vivBirdNoises)} <:VivianPet:790248658054283274>")

    # Mod Commands---------------------------------------------------------------------
    elif command in vivModCommands and author.top_role > mod_role:
      #!raffle <title> <emote>
      if content_lower.startswith(vivModCommands[0]):
        pass
      #!endraffle <title>
      if content_lower.startswith(vivModCommands[0]):
        pass

    #User mentions bot by name
    elif any(word in content_lower for word in vivAttention):
      log.info(f"{author.name} mentioned bot, responding")
      await message.channel.send(random.choice(vivBirdNoises))

    

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
      #Isabelle Stream notification
      role = discord.utils.get(guild.roles, id=932759248755126303)
    elif payload.emoji.id == 794017620965720094:
      #Mark Stream notification
      role = discord.utils.get(guild.roles, id=1024670256381304842)
    
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
      #Isabelle Stream notification
      role = discord.utils.get(guild.roles, id=932759248755126303)
    elif payload.emoji.id == 794017620965720094:
      #Mark Stream notification
      role = discord.utils.get(guild.roles, id=1024670256381304842)
    
    if role is not None:
      member = await guild.fetch_member(payload.user_id)
      if member is not None:
        await member.remove_roles(role)

client.run(os.getenv('TOKEN'))