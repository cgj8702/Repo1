import random

symbols = ['🍒', '🍇', '🍉', '7️']

results = random.choices(symbols, k=3)
print(f'{results[0]} | {results[1]} | {results[2]}')

if results[0] == symbols[3] and results[1] == symbols[3] and results[2] == symbols[3]:
    print('Jackpot! 💰')
else:
    print('Thanks for playing!')
