import os

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Define your server IDs
input_server_id = [1181766217602703510]
output_server_id = 1177348953675665551
channel_id = 1178816186759250110
user_whitelist = [798673042988335144, 1147231541890658356]

versionNum = '1.1.3'

cloneids = 'user_ids.txt'
template = 'message_template.txt'
notes = 'patch_notes.txt'

# Check and create necessary directories and files
if not os.path.exists(cloneids):
    open(cloneids, 'a').close()

if not os.path.exists(template):
    with open(template, 'w') as template_file:
        template_file.write('User IDs:\n{user_ids}')

if not os.path.exists(notes):
    open(notes, 'a').close()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')

# Command to store user IDs
@bot.event
async def on_member_join(member):
    if member.guild.id in input_server_id and member.id not in user_whitelist:
        with open('user_ids.txt', 'r') as file:
            file_content = file.read()
            if f'<@{member.id}>' not in file_content:
                with open('user_ids.txt', 'a') as file2:
                    file2.write(f'<@{member.id}>' + '\n')
                    print('New clone!')

# Command to add user IDs to the txt file
@bot.hybrid_command(name='clone-add', guild=output_server_id, description='Adds the pinged user to the clone list.')
async def clone_add(ctx, user: discord.User):
    user = user.id
    if ctx.guild.id == output_server_id and ctx.channel.id == channel_id:
        if user not in user_whitelist:
            with open('user_ids.txt', 'r') as file:
                file_content = file.read()
                if f'<@{user}>' not in file_content:
                    with open('user_ids.txt', 'a') as file:
                        file.write(f'<@{user}>' + '\n')
                    await ctx.send(f'<@{user}> was added to the Clone List!')
                else:
                    await ctx.send(f'Unable to add <@{user}>, as <@{user}> is already on the clone list.')
        else:
            await ctx.send(f'Unable to add <@{user}>, as that user is unable to be added due to being on the safe-list.')
# Command to clone the list in a specific channel
@bot.hybrid_command(name='clone-list', guild=output_server_id, description='Lists out all known clones.')
async def clone_list(ctx):
    if ctx.guild.id == output_server_id and ctx.channel.id == channel_id:
        with open('user_ids.txt', 'r') as file:
            user_ids = file.readlines()
    
        with open('message_template.txt', 'r') as template_file:
            message_format = template_file.read()
    
        # Replace {user_ids} in the message template
        formatted_message = message_format.replace('{user_ids}', ''.join(user_ids))
    
        # Send the formatted message
        await ctx.send(formatted_message)

@bot.hybrid_command(name='ping', guild=output_server_id, description='Pong!')
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.hybrid_command(name='pong', guild=output_server_id, description='Ping!')
async def pong(ctx):
    await ctx.send("Ping! 🏓")

@bot.hybrid_command(name='version', guild=output_server_id, description='Lists the current bot\'s version!')
async def version(ctx):
    await ctx.send(f"The current bot version is __**{versionNum}**__.")

@bot.hybrid_command(name='patch-notes', guild=output_server_id, description='Tells you the patch notes.')
async def patch_note(ctx):
    if ctx.guild.id == output_server_id and ctx.channel.id == channel_id:
        with open(notes, 'r') as file:
            message = file.readlines()
            message = ''.join(message)
            await ctx.send(f'''# Version {versionNum} patch notes:

{message}''')

# Run the bot with your token
bot.run(os.environ['TOKEN'])
