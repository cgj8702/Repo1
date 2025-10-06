import csv

data_to_write = [
    ['Item', 'Quantity'],
    ['Blender', 2],
    ['Posters', 30],
    ['Shoes', 2],
]

file_path = 'Python 2 Intermediate\\packing_list.csv'

try:
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            print(row)
except FileNotFoundError:
    print('Packing list file not found. Creating a new one.')
    with open(file_path, 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data_to_write)
