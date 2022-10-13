import discord
import os
import random
import logging
import glob
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv

# Logging Configuration----------------------------------------------------
log = logging.getLogger('VivianBot')

console_handler = StreamHandler()
console_handler.setLevel(logging.WARNING)

file_handler = TimedRotatingFileHandler('vivian.log', when='D', interval=1, backupCount=7)
file_handler.setLevel(logging.INFO)

log.addHandler(console_handler)
log.addHandler(file_handler)
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
guild_id = os.getenv('GUILD_ID')
mod_role_id = os.getenv('MOD_ROLE_ID')
testing_channel_id = os.getenv('TESTING_CHANNEL_ID')

# Global variables to hold objects relating to configuration
# Not populated until bot has had a change to run 
guild = None
mod_role = None
# ----------------------------------------------------


# Connect to discord API
client = discord.Client(intents=discord.Intents.all())
    

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
    content_lower = content_lower.lower()
    # for easy use checking against commands
    command = content_lower.split()[0]

    # Enable for very verbose logging
    # log.debug(
    #   f"""Parsing a message: 
    #     Author: {author.name}
    #     Channel: {channel.name}
    #     Content: {content}"""
    # )

    # Format string used to log commands
    log_command = lambda command: log.info(
      f"""Command Recieved: 
        Author: {author.name}
        Channel: {channel.name}
        Command: "{command}" """
    )

    # Format string used to log commands
    log_automated_response = lambda keyword: log.info(
      f"""Keyword Recieved: 
        Author: {author.name}
        Channel: {channel.name}
        Keyword(s): {keyword} """
    )

    # Vivian Commands----------------------------------------------------
    if command in vivAllCommands:
      log_command(command)

      # Global User Commands----------------------------------------------------
      if command in vivGlobalCommands:

        #!pet
        if content_lower.startswith(vivGlobalCommands[0]):
          response = f"{random.choice(vivBirdNoises)} <:VivianPet:790248658054283274>"
      # ----------------------------------------------------

      # Mod Commands----------------------------------------------------
      elif command in vivModCommands and author.top_role > mod_role:

        #!raffle <title> <emote>
        if content_lower.startswith(vivModCommands[0]):
          log.info("<params>")

        #!endraffle <title>
        elif content_lower.startswith(vivModCommands[0]):
          log.info("<params>")
      # ----------------------------------------------------

    # ----------------------------------------------------
    
    # Non-Command Automated Responses----------------------------------------------------
    else:
      # vivAttention----------------------------------------------------
      attention = [word in content_lower for word in vivAttention]
      if any(attention):
        log_automated_response(attention)
        response = random.choice(vivBirdNoises)
        
      # ----------------------------------------------------
    # ----------------------------------------------------

    if command in vivTestingCommands:
      pass # TODO: check if in the right channel, generate some logs
    else:
      await message.channel.send(response)
  except Exception as e:
    log.error(f"Encountered error {e} while processing a message.")
    log.error(f"Message: {message.content} \n Author {message.author.name}")

# reaction add event
@client.event
async def on_raw_reaction_add(payload):
  try:
    msg_id = payload.message_id

    # Pronoun Roles----------------------------------------------------
    if msg_id == 802997626995343370:
      if payload.emoji.id == 802976289379713025:
        # He/Him
        role = discord.utils.get(guild.roles, id=802943259596685332)
      elif payload.emoji.id == 802976289597947914:
        # She/Her
        role = discord.utils.get(guild.roles, id=802943355960164372)
      elif payload.emoji.id == 802976289681834014:
        # They/Them
        role = discord.utils.get(guild.roles, id=802943394409480202)
      else:
        log.warn(f"Server member {member.name} reacted to pronoun roles message with invalid emote")
    # ----------------------------------------------------

    # Game Roles----------------------------------------------------
    elif msg_id == 802997668304650280:
      if payload.emoji.id == 803000326184894496:
        # Art Games
        role = discord.utils.get(guild.roles, id=802943449404801054)
      elif payload.emoji.id == 803000326218317844:
        # OC Questions
        role = discord.utils.get(guild.roles, id=802943523979526174)
      elif payload.emoji.id == 978373881268146256:
        # Gamerz
        role = discord.utils.get(guild.roles, id=978375025461719070)
      else:
        log.warn(f"Server member {member.name} reacted to game roles message with invalid emote")
    # ----------------------------------------------------
      

    # Stream Roles----------------------------------------------------
    elif msg_id == 931991719136878602:
      if payload.emoji.id == 845447895758274631:
        # Isabelle Stream notification
        role = discord.utils.get(guild.roles, id=932759248755126303)
      elif payload.emoji.id == 794017620965720094:
        # Mark Stream notification
        role = discord.utils.get(guild.roles, id=1024670256381304842)
      else:
        log.warn(f"Server member {member.name} reacted to stream roles message with invalid emote")
    # ----------------------------------------------------
      
    if role is not None:
      member = payload.member
      if member is not None:
        await member.add_roles(role)
        log.info(f"Added role {role.name} to server member {member.name}")
      else:
        log.info(f"Attempted to add role {role.name}, but couldn't find original user which requested the addition.")
  except Exception as e:
    log.error(f"Encountered error {e} while processing a raw_reaction_add.")
    log.error(f"Emoji: {payload.emoji.id}\n Member: {payload.member.name}")

# reaction remove event
@client.event
async def on_raw_reaction_remove(payload):
  try:
    msg_id = payload.message_id

    # Pronoun Roles----------------------------------------------------
    if msg_id == 802997626995343370:
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
      else:
        log.warn(f"Server member {member.name} reacted to pronoun roles message with invalid emote")
    # ----------------------------------------------------


    # Game Roles----------------------------------------------------
    elif msg_id == 802997668304650280:
      if payload.emoji.id == 803000326184894496:
        #Art Games
        role = discord.utils.get(guild.roles, id=802943449404801054)
      elif payload.emoji.id == 803000326218317844:
        #OC Questions
        role = discord.utils.get(guild.roles, id=802943523979526174)
      elif payload.emoji.id == 978373881268146256:
        #Gamerz
        role = discord.utils.get(guild.roles, id=978375025461719070)
      else:
        log.warn(f"Server member {member.name} reacted to game roles message with invalid emote")
    # ----------------------------------------------------

    # Stream Roles----------------------------------------------------
    elif msg_id == 931991719136878602:
      if payload.emoji.id == 845447895758274631:
        #Isabelle Stream notification
        role = discord.utils.get(guild.roles, id=932759248755126303)
      elif payload.emoji.id == 794017620965720094:
        #Mark Stream notification
        role = discord.utils.get(guild.roles, id=1024670256381304842)
      else:
        log.warn(f"Server member {member.name} reacted to stream roles message with invalid emote")
    #----------------------------------------------------
      
    if role is not None:
      member = payload.member
      if member is not None:
        await member.remove_roles(role)
        log.info(f"Removed role {role.name} from server member {member.name}")
      else:
        log.info(f"Attempted to remove role {role.name}, but couldn't find original user which requested the addition.")
  except Exception as e:
    log.error(f"Encountered error {e} while processing a raw_reaction_remove.")
    log.error(f"Emoji: {payload.emoji.id}\n Member: {payload.member.name}")

client.run(client_token)