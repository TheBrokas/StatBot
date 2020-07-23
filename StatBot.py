# Work with Python 3.6
import os
import discord
import random
from discord.ext import commands

from dotenv import load_dotenv

import json
import os.path
from os import path

TOKEN = 'NzM1MjI2NTQ5MjgzODQ4MTky.XxdZjw.X2w65mC2vvA8LcTstBhbExz-Tt4'

bot = commands.Bot(command_prefix='!')

client = discord.Client()
#start here 

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!addmatch'):
        if path.exists("StatBotInfo.txt") == True:
            with open('StatBotInfo.txt') as json_file:
                data = json.load(json_file)
            user_message = message.content
            prefix,match_info=user_message.split(' ')
            username = message.author.name 
            #await message.channel.send(content)
            outcome,kda = match_info.split('-')
            kill_str,death_str,assists_str = kda.split('/')
            kill = int(kill_str)
            death = int(death_str)
            assists = int(assists_str)

            if str(username) in data:
                print('user found')
                data[username]['games'] += 1
                data[username]['kills'].append(kill)
                data[username]['deaths'].append(death)
                data[username]['assists'].append(assists)
                if outcome == 'w':
                    data[username]['wins'] += 1  
            else:
                data[username] = {
                    'games': 1,
                    'wins': 0,
                    'kills': [],
                    'deaths': [],
                    'assists': [],
                }
                data[username]['kills'].append(kill)
                data[username]['deaths'].append(death)
                data[username]['assists'].append(assists)
                if outcome.upper() == 'W':
                    data[username]['wins'] += 1      

            await message.channel.send('Match Added')
            with open('StatBotInfo.txt', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            data = {
             }
            await message.channel.send('Statfile was not found, but has been created, try again')
            with open('StatBotInfo.txt', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    if message.content.startswith('!stats'):
        username = message.author.name
        with open('StatBotInfo.txt') as json_file:
            data = json.load(json_file)
            total_kills = data[username]['kills']
            total_kills = sum(total_kills)
            total_deaths = data[username]['deaths']
            total_deaths = sum(total_deaths)
            kd = total_kills / total_deaths
            total_games = data[username]['games']
            total_wins = data[username]['wins']
            win_rate = total_wins / total_games
        stat_reply = '%s, Games Played: %s Winrate: %s KD: %s' % (username, total_games, win_rate, kd)
        await message.channel.send(stat_reply)

    if message.content.startswith('!help'):
        message_reply = '!addmatch to add match. Format it as: !addmatch W-K/D/A where W is Win and L if loss. !stats to check stats. !selfdestruct to close temporarily'
        await message.channel.send(message_reply)

    if message.content.startswith('!selfdestruct'):
        username = message.author.name
        message_reply = "nice try %s" % (username)      
        await message.channel.send(message_reply)
        
client.run(TOKEN)