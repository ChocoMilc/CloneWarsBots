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

# Check and create necessary directories and files
if not os.path.exists('user_ids.txt'):
    open('user_ids.txt', 'a').close()

if not os.path.exists('message_template.txt'):
    with open('message_template.txt', 'w') as template_file:
        template_file.write('User IDs:\n{user_ids}')

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
    if ctx.guild.id == output_server_id and ctx.channel.id == channel_id:
        with open('user_ids.txt', 'r') as file:
            file_content = file.read()
            if f'<@{user}>' not in file_content and user not in user_whitelist:
                with open('user_ids.txt', 'a') as file:
                    file.write(f'<@{user}>' + '\n')
                await ctx.send(f'<@{user}> was added to the Clone List!')
            else:
                await ctx.send(f'Unable to add <@{user}>, as <@{user}> is already on the clone list, or was unable to be added to the list.')

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

# Run the bot with your token
bot.run(os.environ['TOKEN'])


# sus users
# <@796388274826248204>