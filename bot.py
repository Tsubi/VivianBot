import discord
import os
import random
import logging
import glob
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv
from discord.utils import get

# Local file with helpful log message formatters
from log_lambdas import *

# Logging Configuration----------------------------------------------------
log = logging.getLogger('VivianBot')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(formatter)

file_handler = TimedRotatingFileHandler('vivian.log', when='D', interval=1, backupCount=7)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

log.addHandler(console_handler)
log.addHandler(file_handler)
log.setLevel(logging.INFO)
# ----------------------------------------------------


# Vivian Interactions----------------------------------------------------
#Listen words - bot will respond when one is menioned
vivAttention = ["vivian", "virb", "birb"]
# Global commands - any user can use these
vivGlobalCommands = ["!pet"]
# Mod commands - need minimum mod permissions to use
vivModCommands = ["!raffle", "!endraffle"]
# Testing commands - used to note commands that may only be used in bot channel for test purposes
vivTestingCommands = ["!raffle", "!endraffle"]

# Full list of commands, for control flow
vivAllCommands = vivGlobalCommands + vivModCommands

# Pet Responses, used to respond to vivAttention as well
vivBirdNoises = ["Chirp!", "Cheep!", "Peep peep!", "Chirp chirp!", "Tweet tweet!"]
# ----------------------------------------------------


# Load data from environment----------------------------------------------------
# Active raffles. Stored as a list of user ids.
raffles = {}
for file in glob.glob("*.raffle"):
  raffle_name = os.path.splitext(file)[0]
  raffle_entrants = []
  with open(file) as f:
    raffle_entrants = f.read().split()
  raffles[raffle_name] = raffle_entrants

#Loading .env file, contains sensitive client information, and other server-configuration
load_dotenv()
client_token = os.getenv('TOKEN')
guild_id = int(os.getenv('GUILD_ID'))
mod_role_id = int(os.getenv('MOD_ROLE_ID'))
testing_channel_id = int(os.getenv('TESTING_CHANNEL_ID'))

# Global variables to hold objects relating to configuration
# Not populated until bot has had a chance to run 
guild = None
mod_role = None
# ----------------------------------------------------


# Connect to discord API
intents = discord.Intents.all()
client = discord.Client(intents=intents)
    

# Post-login startup sequence
@client.event
async def on_ready():
  log.info(f'Bot logged in as: {client.user}')

  # Setup global variables now that we are logged in
  global guild, mod_role
  guild = client.get_guild(guild_id)
  mod_role = guild.get_role(mod_role_id) 

# message sent event
@client.event
async def on_message(message):



  try:
    if message.author == client.user:
        return
    # get information about who sent the message
    author = message.author

    # where the message was sent
    channel = message.channel

    #the message content variable, string representation
    content = message.content
    # for easy use in string matching
    content_lower = content.lower()
    # for easy use checking against commands
    command = content_lower.split()[0]

    # Guaruntee the response is defined, even if it is None
    response = None

    # Enable for very verbose logging
    # log.debug(
    #   f"""Parsing a message: 
    #     Author: {author.name}
    #     Channel: {channel.name}
    #     Content: {content}"""
    # )

    # Vivian Commands----------------------------------------------------
    if command in vivAllCommands:
      log_command(message, command)

      # Global User Commands----------------------------------------------------
      if command in vivGlobalCommands:

        #!pet
        if content_lower.startswith(vivGlobalCommands[0]):
          response = f"{random.choice(vivBirdNoises)} <:VivianPet:790248658054283274>"
      # ----------------------------------------------------

      # Mod Commands----------------------------------------------------
      elif command in vivModCommands and ( author.top_role > mod_role or 
        ( command in vivTestingCommands and channel.id==testing_channel_id ) ):


        #!raffle <title> <emote>
        if content_lower.startswith(vivModCommands[0]):
          raise NotImplementedError()

        #!endraffle <title>
        elif content_lower.startswith(vivModCommands[0]):
          raise NotImplementedError()
      # ----------------------------------------------------

    # ----------------------------------------------------
    
    # Non-Command Automated Responses----------------------------------------------------
    else:
      # vivAttention----------------------------------------------------
      attention = [word for word in vivAttention if word in content_lower]
      if any(attention):
        log_automated_response(message, attention)
        response = random.choice(vivBirdNoises)
        
      # ----------------------------------------------------
    # ----------------------------------------------------

    if command in vivTestingCommands:
      pass # TODO: check if in the right channel, generate some logs. Retu


    # Only send a response if we have one to send.
    # Some commands may need to do logic with the message they send (such as get the ID)
    if response != None:
      await message.channel.send(response)
  except Exception as e:
    log_message_error(message, e)

# reaction add event
@client.event
async def on_raw_reaction_add(payload):
  try:
    msg_id = payload.message_id
    emoji_id = payload.emoji.id
    member = payload.member
    role = None

    # Pronoun Roles----------------------------------------------------
    if msg_id == 802997626995343370:
      
      if emoji_id == 802976289379713025:
        # He/Him
        role = discord.utils.get(guild.roles, id=802943259596685332)
      elif emoji_id == 802976289597947914:
        # She/Her
        role = discord.utils.get(guild.roles, id=802943355960164372)
      elif emoji_id == 802976289681834014:
        # They/Them
        role = discord.utils.get(guild.roles, id=802943394409480202)
      else:
        log_invalid_emoji(payload, "Pronoun")
    # ----------------------------------------------------

    # Game Roles----------------------------------------------------
    elif msg_id == 802997668304650280:
      if emoji_id == 803000326184894496:
        # Art Games
        role = discord.utils.get(guild.roles, id=802943449404801054)
      elif emoji_id == 803000326218317844:
        # OC Questions
        role = discord.utils.get(guild.roles, id=802943523979526174)
      elif emoji_id == 978373881268146256:
        # Gamerz
        role = discord.utils.get(guild.roles, id=978375025461719070)
      else:
        log_invalid_emoji(payload, "Game")
    # ----------------------------------------------------
      

    # Stream Roles----------------------------------------------------
    elif msg_id == 931991719136878602:
      if emoji_id == 845447895758274631:
        # Isabelle Stream notification
        role = discord.utils.get(guild.roles, id=932759248755126303)
      elif emoji_id == 794017620965720094:
        # Mark Stream notification
        role = discord.utils.get(guild.roles, id=1024670256381304842)
      else:
        log_invalid_emoji(payload, "Stream")
    # ----------------------------------------------------
      
    if role is not None:
      member = payload.member
      if member is not None:
        await member.add_roles(role)
        log_add_role(member, role)
      else:
        log.error(f"Attempted to add a role to a member that doesn't exist???")
  except Exception as e:
    log_reaction_error(payload, e)

# reaction remove event
@client.event
async def on_raw_reaction_remove(payload):
  try:
    # Refresh guild, to refresh members
    global guild
    guild = await client.fetch_guild(payload.guild_id)
    
    msg_id = payload.message_id
    emoji_id = payload.emoji.id
    member = await guild.fetch_member(payload.user_id)
    role = None

    # Pronoun Roles----------------------------------------------------
    if msg_id == 802997626995343370:
      if emoji_id == 802976289379713025:
        #He/Him
        role = discord.utils.get(guild.roles, id=802943259596685332)
      elif emoji_id == 802976289597947914:
        #She/Her
        role = discord.utils.get(guild.roles, id=802943355960164372)
      elif payload.emoji.id == 802976289681834014:
        #They/Them
        role = discord.utils.get(guild.roles, id=802943394409480202)
      else:
        log_invalid_emoji(payload, "Pronoun")
    # ----------------------------------------------------


    # Game Roles----------------------------------------------------
    elif msg_id == 802997668304650280:
      if emoji_id == 803000326184894496:
        #Art Games
        role = discord.utils.get(guild.roles, id=802943449404801054)
      elif emoji_id == 803000326218317844:
        #OC Questions
        role = discord.utils.get(guild.roles, id=802943523979526174)
      elif emoji_id == 978373881268146256:
        #Gamerz
        role = discord.utils.get(guild.roles, id=978375025461719070)
      else:
        log_invalid_emoji(payload, "Game")
    # ----------------------------------------------------

    # Stream Roles----------------------------------------------------
    elif msg_id == 931991719136878602:
      if emoji_id == 845447895758274631:
        #Isabelle Stream notification
        role = discord.utils.get(guild.roles, id=932759248755126303)
      elif emoji_id == 794017620965720094:
        #Mark Stream notification
        role = discord.utils.get(guild.roles, id=1024670256381304842)
      else:
        log_invalid_emoji(payload, "Stream")
    #----------------------------------------------------
      
    if role is not None:
      if member is not None:
        await member.remove_roles(role)
        log_remove_role(member, role)
      else:
        log.error(f"Attempted to remove a role from a member that could not be found ({payload.user_id})")
  except Exception as e:
    log_reaction_error(payload, e)

client.run(client_token)