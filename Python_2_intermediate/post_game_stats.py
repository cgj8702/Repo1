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

pat = player_list[0]
mar = player_list[1]
trav = player_list[2]


for player in player_list:
    name = player['name']
    position = player['position']
    print(f'{name} plays {position}')

print()
print('Players\' positions:')

for player in player_list:
    print(player['position'])

pat['touchdowns'] = 5
print()
print('Update:', pat['name'], 'now has', pat['touchdowns'], 'touchdowns')
print()

total_touchdowns = int((pat['touchdowns'] + mar['touchdowns'] + trav['touchdowns']))
print('Total touchdowns:', total_touchdowns)
num_players = len(player_list)
print('Divided by', num_players, 'players equals...')
avg_touchdowns = int(total_touchdowns / num_players)
print('Average touchdowns:', avg_touchdowns)
