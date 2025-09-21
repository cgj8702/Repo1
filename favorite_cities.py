class Cities:
    def __init__(self, name, country, population, landmarks):
        self.name = name
        self.country = country
        self.population = population
        self.landmarks = landmarks


hometown = Cities('Hometown', 'USA', 30000, 'Old Well, Duke Chapel, Franklin Street')

destination = Cities('Destination', 'Foreign Country', 100000, 'Landmarks 1, 2, 3')

print(vars(hometown))
print(vars(destination))
