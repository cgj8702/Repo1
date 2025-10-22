menu = ['Cheeseburger', 'French fries', 'Soda', 'Ice cream', 'Cookie']


def get_item(x):
    if x == 1:
        return menu[x - 1]
    elif x == 2:
        return menu[x - 1]
    elif x == 3:
        return menu[x - 1]
    elif x == 4:
        return menu[x - 1]
    elif x == 5:
        return menu[x - 1]
    else:
        print('Error')


def welcome():
    print('Here is our menu: ')
    for i in range(1, 6):
        print(f'{i}. {menu[i - 1]}')


welcome()

option = int(input('What would you like to order? '))
print(get_item(option))
