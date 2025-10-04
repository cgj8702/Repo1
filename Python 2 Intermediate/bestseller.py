import csv
from encodings import utf_8

csv_file_path = 'Python 2 Intermediate\\Bestseller.csv'
best_selling_book = None
max_sales = 0

with open(csv_file_path, 'r', encoding='utf_8') as csv_file:
    csv_reader = csv.reader(csv_file)
    csv_file.readline()
    for row in csv_reader:
        current_sales = float(row[4])
        if current_sales > max_sales:
            max_sales = current_sales
            best_selling_book = row
