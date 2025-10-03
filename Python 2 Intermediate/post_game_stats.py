# Write code below 💖

player_list = [
    {
        'name': 'Patrick Mahomes',
        'position': 'Quarterback',
        'jersey_number': 15,
        'yards_gained': 270,
        'touchdowns': 4,
    },
    {
        'name': 'Marquise Brown',
        'position': 'Wide Receiver',
        'jersey_number': 5,
        'yards_gained': 38,
        'touchdowns': 1,
    },
    {
        'name': 'Travis Kelce',
        'position': 'Tight End',
        'jersey_number': 87,
        'yards_gained': 48,
        'touchdowns': 0,
    },
]


for i in player_list:
    names = i['name']


names_list = [i['name'] for i in player_list]

# names = [player["name"] for player in player_list]

# print('Players\' names:', end=" ")
# for i in player_list:
#    print(i['name'], sep=",", end="")


# print(pat['position'])
# print(mar['position'])
# print(trav['position'])

# trav['touchdowns'] = 1
# print(trav['touchdowns'])

# avg_touchdowns = int((pat['touchdowns'] + mar['touchdowns'] + trav['touchdowns']) / 3)
# print(avg_touchdowns)
