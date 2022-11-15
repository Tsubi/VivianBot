import logging

log = logging.getLogger('VivianBot')

# Log generated for a failure during message parsing
log_message_error = lambda message, error: log.error(
f"""Message Parsing Failed!:
    Author: {message.author.name} ({message.author.id})
    Channel: {message.channel.name}
    Error: {error}
    Message: "{message.content}" ({message.id}) """
)

# Log generated when a command is detected
log_command = lambda message, command: log.info(
    f"""Command Recieved: 
    Author: {message.author.name} ({message.author.id})
    Channel: {message.channel.name}
    Command: "{command}" """
)

# Log generated when a 'keyword' is detected
log_automated_response = lambda message, keyword: log.info(
    f"""Keyword Recieved: 
    Author: {message.author.name} ({message.author.id})
    Channel: {message.channel.name}
    Keyword(s): {keyword} """
)

log_reaction_error = lambda payload, error: log.error(
f"""Reaction Parsing Failed!:
    Author: {payload.member.name} ({payload.member.id})
    Message: {payload.message_id}
    Emote: {payload.emoji.id} """
)

# Invalid Emoji was used on a Role-Add message
log_invalid_emoji = lambda payload, role_type: log.warn(
  f"""Invalid Emoji Recieved for Role Change: 
    Member: {payload.member.name} ({payload.member.id})
    Role Type: {role_type}
    Emote: {payload.emoji.id} """
)

log_add_role = lambda member, role: log.info(
f"""Role added to member: 
    Member: {member.name} ({member.id})
    Role: {role.name} """
)

log_remove_role = lambda member, role: log.info(
f"""Role removed from member: 
    Member: {member.name} ({member.id})
    Role Id: {role.name} """
)