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

cloneids = 'user_ids.txt'
template = 'message_template.txt'
notes = 'patch_notes.txt'
versionFile = 'version_number.txt'

if not os.path.exists(versionFile):
    with open(versionFile, 'w') as version_file:
        version_file.write('1.0.0')

with open(versionFile, 'r') as version_file:
    versionNum = version_file.read()

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
    print(f'Logged in as {bot.user.name}, with version {versionNum} .')

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

@bot.event
async def on_message(ctx):
    if not ctx.author == bot.user:
        if ctx.guild is None:
            await ctx.reply('Message has been forwarded to <@798673042988335144>!')
            target_user = bot.get_user(int(798673042988335144))
            # Send a direct message to the target user with the variable
            await target_user.send(f'''User <@{ctx.author.id}> sent:
>>> {ctx.content}''')

# Command to add user IDs to the txt file
@bot.hybrid_command(name='clone-add', guild=output_server_id, description='Adds the pinged user to the clone list.')
async def clone_add(ctx, user: discord.User):
    user = user.id
    if ctx.guild.id == output_server_id and ctx.channel.id == channel_id:
        print('Add Clone')
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
        print('Clone List')
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
    print('Ping')
    await ctx.send("Pong! 🏓")

@bot.hybrid_command(name='version', guild=output_server_id, description='Lists the current bot\'s version!')
async def version(ctx):
    print('Version')
    with open(versionFile, 'r') as version_file:
        versionNum = version_file.read()
    await ctx.send(f"The current bot version is __**{versionNum}**__.")

@bot.hybrid_command(name='patch-notes', guild=output_server_id, description='Tells you the patch notes.')
async def patch_note(ctx):
    if ctx.guild.id == output_server_id and ctx.channel.id == channel_id:
        with open(versionFile, 'r') as version_file:
            versionNum = version_file.read()
        print('Patch Notes')
        with open(notes, 'r') as file:
            message = file.readlines()
            message = ''.join(message)
            await ctx.send(f'''# Version {versionNum} patch notes:

{message}''')

@bot.hybrid_command(name='suggest', guild=output_server_id, description='Suggests an idea.')
async def suggest(ctx):
    await ctx.send(f'If you have a suggestion, DM <@{bot.user.id}> your suggestion!')

def is_me(m):
    return m.author == bot.user

@bot.hybrid_command(name='clean', guild=output_server_id, description='Cleans bot messages from channel.')
async def clean(ctx):
    await ctx.channel.purge(limit=100, check=is_me)
    await ctx.send('Finished cleaning bot messages!')
    
# Run the bot with your token
bot.run(os.environ['TOKEN'])
