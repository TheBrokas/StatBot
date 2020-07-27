#Takes discord inputs and generates outputs accordingly
import os
import discord
import random
from discord.ext import commands
import re
import json
import os.path
from os import path
from GraphGeneration import generate_daily_graph
import time

print('Bot Activated')
with open('token.txt') as token_file:
    token_id = json.load(token_file)
TOKEN = token_id

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
            try:
                prefix,match_info=user_message.split(' ')
            except:
                print('value error msg')
                await message.channel.send('Invalid input, try again.')
            else:
                username = str(message.author.id)
                #await message.channel.send(content)
                try:
                    outcome,kda = match_info.split('-')
                except:
                    print('value error msg')
                    await message.channel.send('Invalid input, try again.')
                else:
                    try:
                        kill_str,death_str,assists_str = kda.split('/')
                    except:
                        print('value error msg')
                        await message.channel.send('Invalid input, try again.')
                    if kill_str.isnumeric() and death_str.isnumeric() and assists_str.isnumeric():
                        kill = abs(int(kill_str))
                        death = abs(int(death_str))
                        assists = abs(int(assists_str))
                        if str(username) in data:
                            print('user found')
                            data[username]['username'] = re.sub(r'\W+', '', message.author.name)
                            data[username]['games'] += 1
                            data[username]['kills'].append(kill)
                            data[username]['deaths'].append(death)
                            data[username]['assists'].append(assists)
                            if outcome.upper() == 'W':
                                data[username]['wins'] += 1
                            if outcome.upper == 'L':
                                data[username]['losses'] += 1
                            if outcome.upper == 'T':
                                data[username]['ties'] += 1
                        else:
                            data[username] = {
                                'username': re.sub(r'\W+', '', message.author.name),
                                'games': 1,
                                'wins': 0,
                                'losses': 0,
                                'ties': 0,
                                'kills': [],
                                'deaths': [],
                                'assists': [],
                            }
                            data[username]['kills'].append(kill)
                            data[username]['deaths'].append(death)
                            data[username]['assists'].append(assists)
                            if outcome.upper() == 'W':
                                data[username]['wins'] += 1
                            if outcome.upper == 'L':
                                data[username]['losses'] += 1
                            if outcome.upper == 'T':
                                data[username]['ties'] += 1

                        await message.channel.send('Match Added.')
                        with open('StatBotInfo.txt', 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                    else:
                        await message.channel.send('Invalid formating, try again.')
        else:
            data = {
             }
            await message.channel.send('Statfile was not found, but has been created, try again')
            with open('StatBotInfo.txt', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    if message.content == '!mystats':
        username = str(message.author.id)
        with open('StatBotInfo.txt') as json_file:
            data = json.load(json_file)
            name,win_rate,kd,total_games = stat_calculator(data[username]['username'],data[username]['kills'],data[username]['deaths'],data[username]['games'],data[username]['wins'])
        stat_reply = '%s: \nGames Played: %s \nWin Percent: %s \nKD: %s' % (name, total_games, win_rate, kd)
        await message.channel.send(stat_reply)

    if message.content.startswith('!stats'):
        find_user = message.content
        prefix,username = find_user.split(' ')
        with open('StatBotInfo.txt') as json_file:
            data = json.load(json_file)
            if str(username) in data:
                with open('StatBotInfo.txt') as json_file:
                    name,win_rate,kd,total_games = stat_calculator(data[username]['username'],data[username]['kills'],data[username]['deaths'],data[username]['games'],data[username]['wins'])
                stat_reply = '%s: \nGames Played: %s \nWin Percent: %s \nKD: %s' % (name, total_games, win_rate, kd)
                await message.channel.send(stat_reply)
            else:
                await message.channel.send('User not found')

    if message.content.startswith('!help'):
        message_reply = '!addmatch to add match. Format it as: !addmatch W-K/D/A where W is Win and L if loss. \n!mystats to check own stats. \n"!stats userid" to find user stats. \n!selfdestruct to close temporarily. \n!graphs for help with graphs.'
        await message.channel.send(message_reply)

    if message.content.startswith('!graphs'):
        message_reply = "!dailygraph STAT to see graph of stats. Replace STAT with items such as wins, losses, ties, kills, deaths, assists, KD, win rate."
        await message.channel.send(message_reply)

    if message.content.startswith('!selfdestruct'):
        username = re.sub(r'\W+', '', message.author.name)
        message_reply = "nice try %s" % (username)
        await message.channel.send(message_reply)

    if message.content.startswith('!dailygraph'):
        user_name = message.author.name
        username = str(message.author.id)
        user_message = message.content
        prefix,stat = user_message.split(' ')
        if stat == 'wins' or stat == 'losses' or stat == 'ties' or stat == 'kills' or stat == 'deaths' or stat == 'assists' or stat == 'KD' or stat == 'winrate':
            file_location,plt = generate_daily_graph(username,stat,user_name)
            await message.channel.send(file=discord.File(file_location))
            plt.clf
            time.sleep(3)
            os.remove(file_location)
        else:
            await message.channel.send('Invalid request. You are can request: wins, losses, ties, kills, deaths, assists, KD, winrate.')



def stat_calculator(names,kills,deaths,games,wins):
        name = names
        total_kills = kills
        total_kills = sum(total_kills)
        total_deaths = deaths
        total_deaths = sum(total_deaths)
        total_games = games
        total_wins = wins
        win_rate = total_wins / total_games * 100
        if total_deaths > 0:
            kd = total_kills / total_deaths
            kd = round(kd,2)
        else:
            kd = total_kills
        return name,win_rate,kd,total_games

client.run(TOKEN)