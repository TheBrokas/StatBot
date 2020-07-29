#Generates Graphs from txt files
import json
import os
import os.path
from os import path
import matplotlib
import matplotlib.pyplot as plt

discord_background_color = '#36393f'

def generate_daily_graph(user_id,stat,user_name):
    with open('daily_data.txt') as json_file:
        daily_data = json.load(json_file)
    data = daily_data[user_id][stat]
    plt.style.use('dark_background')
    fig = plt.figure()
    ax = plt.gca()
    fig.patch.set_facecolor(discord_background_color)
    ax.set_facecolor(discord_background_color)
    plt.plot(*zip(*sorted(data.items())), marker = 'o')
    plot_title = user_name + ': ' + stat + ' -DailyGraph'
    plt.title(plot_title)
    plt.xlabel('DAY')
    plt.ylabel(stat.upper())
    plt.ylim(ymin=0)
    file_location = str(user_id) + '_' + str(stat) + '_graph.png'
    plt.savefig(file_location, facecolor=fig.get_facecolor(),edgecolor='none')
    return file_location, plt.figure()
generate_daily_graph('90559730715467776','kills','mtb')
