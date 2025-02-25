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
from datetime import datetime

print('Bot Activated')
with open('token.txt') as token_file:
    token_id = json.load(token_file)
TOKEN = token_id

bot = commands.Bot(command_prefix='!')

client = discord.Client()
#start here

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.content.startswith('!addmatch'):
        save_input(message)
        if path.exists("StatBotInfo.txt") == True:
            with open('StatBotInfo.txt') as json_file:
                data = json.load(json_file)
                try: kill,death,assists,outcome,userid,username = split_user_input(message)
                except: await message.channel.send('Invalid input, try again.')
                if str(userid) in data:
                    data[userid]['username'] = re.sub(r'\W+', '', message.author.name)
                    data[userid]['games'] += 1
                    update_stats_from_input(data,userid,kill,death,assists,outcome)
                else:
                    data[userid] = {
                        'username': re.sub(r'\W+', '', message.author.name),
                        'games': 1,
                        'wins': 0,
                        'losses': 0,
                        'ties': 0,
                        'kills': [],
                        'deaths': [],
                        'assists': [],
                    }
                    update_stats_from_input(data,userid,kill,death,assists,outcome)
                await message.channel.send('Match Added.')
                with open('StatBotInfo.txt', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            data = {
             }
            await message.channel.send('Statfile was not found, but has been created, try again')
            with open('StatBotInfo.txt', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    if message.content == '!mystats':
        userid,username = message_username_userid(message)
        with open('StatBotInfo.txt') as json_file:
            data = json.load(json_file)
            name,win_rate,kd,total_games = stat_calculator(data[userid]['username'],data[userid]['kills'],data[userid]['deaths'],data[userid]['games'],data[userid]['wins'])
        stat_reply = '%s: \nGames Played: %s \nWin Percent: %s \nKD: %s' % (name, total_games, win_rate, kd)
        await message.channel.send(stat_reply)

    if message.content.startswith('!stats'):
        find_user = message.content
        _prefix,userid = find_user.split(' ')
        with open('StatBotInfo.txt') as json_file:
            data = json.load(json_file)
            if str(userid) in data:
                with open('StatBotInfo.txt') as json_file:
                    name,win_rate,kd,total_games = stat_calculator(data[userid]['username'],data[userid]['kills'],data[userid]['deaths'],data[userid]['games'],data[userid]['wins'])
                stat_reply = '%s: \nGames Played: %s \nWin Percent: %s \nKD: %s' % (name, total_games, win_rate, kd)
                await message.channel.send(stat_reply)
            else:
                await message.channel.send('User not found')

    if message.content.startswith('!help'):
        message_reply = '**!addmatch *outcome*-*kills*/*deaths*/*assists* ** to add match. ex: !addmatch W-19/12/5 where W is win, L if loss, T if tie.\
        \n**!mystats** to check own stats.\
        \n**!stats *userid* ** to find user stats, where userid is a users discord id.\
        \n**!selfdestruct** to close temporarily.\
        \n**!graphs** for help with graphs.'
        await message.channel.send(message_reply)

    if message.content.startswith('!graphs'):
        message_reply = "**!dailygraph *stat* ** to see graph of stats. Replace *stat* with items such as wins, losses, ties, kills, deaths, assists, KD, winrate."
        await message.channel.send(message_reply)

    if message.content.startswith('!selfdestruct'):
        userid,username = message_username_userid(message)
        message_reply = "nice **try** %s aka %s" % (username,userid)
        await message.channel.send(message_reply)

    if message.content.startswith('!dailygraph'):
        userid,username = message_username_userid(message)
        user_message = message.content
        _prefix,stat = user_message.split(' ')
        if stat == 'wins' or stat == 'losses' or stat == 'ties' or stat == 'kills' or stat == 'deaths' or stat == 'assists' or stat == 'KD' or stat == 'winrate':
            file_location,plt = generate_daily_graph(userid,stat,username)
            await message.channel.send(file=discord.File(file_location))
            plt.clf
            time.sleep(3)
            os.remove(file_location)
        else:
            await message.channel.send('Invalid request. You are can request: wins, losses, ties, kills, deaths, assists, KD, winrate.')

    if message.content.startswith('!delmatch'):
        try: kill,death,assists,outcome,userid,username = split_user_input(message)
        except: await message.channel.send('Invalid input, try again.')
        else:
            remove_matchadd(userid,kill,death,assists,outcome)
            await message.channel.send('Match Deleted')

def stat_calculator(names,kills,deaths,games,wins): #Calculate stats
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

def update_stats_from_input(data,userid,kills,deaths,assists,game_outcome): #Updates the stats from the user input. 
    data[userid]['kills'].append(kills)
    data[userid]['deaths'].append(deaths)
    data[userid]['assists'].append(assists)
    if game_outcome.upper() == 'W':data[userid]['wins'] += 1
    if game_outcome.upper() == 'L':data[userid]['losses'] += 1
    if game_outcome.upper() == 'T':data[userid]['ties'] += 1

def message_username_userid(message): #Finds the messangers username and userid
    userid = str(message.author.id)
    username = re.sub(r'\W+', '', message.author.name)
    return userid,username

def remove_matchadd(userid,kill,death,assist,game_outcome): #Removes specified match
    with open('StatBotInfo.txt') as json_file:
        data = json.load(json_file)
        data[userid]['kills'].remove(kill)
        data[userid]['deaths'].remove(death)
        data[userid]['assists'].remove(assist)
        if game_outcome.upper() == 'W':data[userid]['wins'] -= 1
        if game_outcome.upper() == 'L':data[userid]['losses'] -= 1
        if game_outcome.upper() == 'T':data[userid]['ties'] -= 1
        with open('StatBotInfo.txt', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def split_user_input(message): #Takes the user input and divides it into corresponding variables.
    user_message = message.content
    _prefix,match_info=user_message.split(' ')
    userid,username = message_username_userid(message)
    outcome,kda = match_info.split('-')
    kill_str,death_str,assists_str = kda.split('/')
    kill = abs(int(kill_str))
    death = abs(int(death_str))
    assists = abs(int(assists_str))
    return kill,death,assists,outcome,userid,username

def save_input(message): #Saves the user command input
    if path.exists('UserInputs.txt') == False:
        user_inputs = {}
        with open('UserInputs.txt', 'w', encoding='utf-8') as f:
            json.dump(user_inputs, f, ensure_ascii=False, indent=4)

    userid,_username = message_username_userid(message)
    current_date  = datetime.date(datetime.now())
    current_date = str(current_date)
    user_message = message.content
    with open('UserInputs.txt') as json_file:
        user_inputs = json.load(json_file)
    if str(userid) not in user_inputs: user_inputs[userid] = {}
    if current_date not in user_inputs[userid]: user_inputs[userid][current_date] = [user_message]  
    else: user_inputs[userid][current_date].append(user_message)

    with open('UserInputs.txt', 'w', encoding='utf-8') as f:
        json.dump(user_inputs, f, ensure_ascii=False, indent=4)
   
client.run(TOKEN)