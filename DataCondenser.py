#Converts data into daily and weekly compressions
import json
import os
import os.path
from os import path

#Daily Data Compression
current_day = 0
if path.exists("StatBotInfo.txt") == True:
     with open('StatBotInfo.txt') as json_file:
         data_dict = json.load(json_file)
    
if path.exists('daily_data.txt') == False:
    daily_data = {
    }
    print("Creating New Path")
else:
    print("Path found")
    with open('daily_data.txt') as json_file:
        daily_data = json.load(json_file)
        for key in data_dict:
            if str(key) in daily_data:
                print("user found")
            else:
                print("new user")
                daily_data[key] = {
                    'username': {},
                    'games played': {},
                    'wins': {},
                    'losses': {},
                    'ties': {},
                    'kills': {},
                    'deaths': {},
                    'assists': {},
            }
            username = data_dict[key]['username']
            game_count = data_dict[key]['games']
            win_count = data_dict[key]['wins']
            loss_count = data_dict[key]['losses']
            tie_count = data_dict[key]['ties']
            kill_count = sum(data_dict[key]['kills'])
            death_count = sum(data_dict[key]['deaths'])
            assist_count = sum(data_dict[key]['assists'])
            daily_data[key]['username'] = username
            daily_data[key]['games played'] = {current_day:game_count}
            daily_data[key]['wins'][current_day] = win_count
            daily_data[key]['losses'][current_day] = loss_count
            daily_data[key]['ties'][current_day] = tie_count
            daily_data[key]['kills'][current_day] = kill_count
            daily_data[key]['deaths'][current_day] = death_count
            daily_data[key]['assists'][current_day] = assist_count

with open('daily_data.txt', 'w+', encoding='utf-8') as f:
     json.dump(daily_data, f, ensure_ascii=False, indent=3)