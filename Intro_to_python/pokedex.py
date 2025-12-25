class Pokemon:
    def __init__(self, entry, name, types, description, is_caught):
        self.entry = entry
        self.name = name
        self.types = types
        self.description = description
        self.is_caught = is_caught

    def speak(self):
        print(self.name + ', ' + self.name + '!')

    def display_details(self):
        print('Entry Number: ' + str(self.entry))
        print('Name: ' + self.name)
        if len(self.types) == 1:
            print('Type: ' + self.types[0])
        else:
            print('Types: ' + self.types[0] + ' and ' + self.types[1])
        print('Description: ' + self.description)
        if self.is_caught:
            print(self.name + ' has been caught!')
        else:
            print(self.name + ' has not been caught yet.')


pikachu = Pokemon(
    25,
    'Pikachu',
    ['Electric'],
    'It has small electric sacs on both its cheeks. If threatened, it looses electric charges from the sacs.',
    False,
)

bulby = Pokemon(
    1,
    'Bulbasaur',
    ['Grass', 'Poison'],
    'For some time after its birth, it uses the nutrients that are packed into the seed on its back in order to grow.',
    True,
)

charmy = Pokemon(
    4,
    'Charmander',
    ['Fire'],
    'The flame on its tail shows the strength of its life-force. If Charmander is weak, the flame also burns weakly.',
    False,
)


pikachu.display_details()
bulby.display_details()
charmy.speak()
