#Converts data into daily and weekly compressions
import json
import os
import os.path
from os import path

#Daily Data Compression

if path.exists("StatBotInfo.txt") == True:
     with open('StatBotInfo.txt') as json_file:
         data_dict = json.load(json_file)
    
daily_data = {
}

current_day = 0
# data_dict = {
#     "90559730715467776": {
#         "username": "MtB_",
#         "games": 13,
#         "wins": 5,
#         "losses": 0,
#         "ties": 0,
#         "kills": [12,4,19,20],
#         "deaths": [16,17,19,17],
#         "assists": [2,4,11,2]}  
# }

for key in data_dict:
    print(key)
    username = data_dict[key]['username']
    game_count = data_dict[key]['games']
    win_count = data_dict[key]['wins']
    loss_count = data_dict[key]['losses']
    tie_count = data_dict[key]['ties']
    kill_count = sum(data_dict[key]['kills'])
    death_count = sum(data_dict[key]['deaths'])
    assist_count = sum(data_dict[key]['assists'])
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

    daily_data[key]['username'] = username
    daily_data[key]['games'] = {current_day: game_count}
    daily_data[key]['wins'][current_day] = win_count
    daily_data[key]['losses'][current_day] = loss_count
    daily_data[key]['ties'][current_day] = tie_count
    daily_data[key]['kills'][current_day] = kill_count
    daily_data[key]['deaths'][current_day] = death_count
    daily_data[key]['assists'][current_day] = assist_count


print(daily_data)
with open('StatBotInfo.txt', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)