#Converts data into daily and weekly compressions
import json
import os
import os.path
import datetime
import shutil
from os import path

#pull the current day from txt file
with open('daycount.txt') as day_count_file:
    current_day = json.load(day_count_file)

#checks if user input file exists
if path.exists("StatBotInfo.txt") == True:
     with open('StatBotInfo.txt') as json_file:
         data_dict = json.load(json_file)

#checks if daily_data.txt exists, if it doesnt, it generetes a empty daily_data dict. 
#if daily_data dict already exists, it pull it from the txt file.
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
            
with open('daily_data.txt', 'w+', encoding='utf-8') as f:
     json.dump(daily_data, f, ensure_ascii=False, indent=3)
if path.exists("StatBotInfo.txt") == True:
    source = "StatBotInfo.txt"
    destination = "DataStorage"
    new_path = shutil.move(source,destination)
    Current_date = datetime.datetime.today().strftime ('%d-%b-%Y')
    os.rename(r'C:\Users\dargi\Desktop\Coding\ValorantBot\DataStorage\StatBotInfo.txt',r'C:\Users\dargi\Desktop\Coding\ValorantBot\DataStorage\StatBotInfo_day' + str(current_day)+ '_' + str(Current_date) + '.txt')