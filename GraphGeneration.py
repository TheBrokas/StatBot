#Generates Graphs from txt files
import json
import os
import os.path
from os import path
import matplotlib
import matplotlib.pyplot as plt

# plt.plot([0,1,2,3,4],[0,3,5,9,11])
# plt.xlabel('Months')
# plt.ylabel('Numbers')
# plt.show()


# data = {1: 10,
#     2: 15,
#     3: 11,
#     4: 24
# }
def generate_daily_graph(user_id,stat):
    with open('daily_data.txt') as json_file:
        daily_data = json.load(json_file)
    data = daily_data[user_id][stat]
    plt.style.use('dark_background')
    plt.plot(*zip(*sorted(data.items())), marker = 'o')
    plt.xlabel('Day')
    plt.ylabel(stat.upper())
    plt.ylim(ymin=0)
    file_location = str(user_id) + '_' + str(stat) + '_graph.png'
    plt.savefig(file_location)
    return file_location, plt.figure()
#generate_daily_graph('90559730715467776','kills')
