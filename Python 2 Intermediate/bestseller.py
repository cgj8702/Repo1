import csv
from encodings import utf_8
import ast

csv_file_path = 'Python 2 Intermediate\\Bestseller.csv'
best_selling_book = None
max_sales = 0

with open(csv_file_path, 'r', encoding='utf_8') as csv_file:
    csv_reader = csv.reader(csv_file)
    csv_file.readline()  # reads first line in order to skip it in the for loop
    for row in csv_reader:
        current_sales = float(
            row[4]
        )  # column 4 is where the data is located, sets variable to sales number
        if (
            current_sales > max_sales
        ):  # max is initialized at 0 so it compares first row sales number, then loops through to compare higher sales numbers
            max_sales = current_sales  # sets max to current sales
            best_selling_book = row  # sets current row to best selling
            # loops through to end with the best selling variable set to the row with the highest number of sales
    print(
        best_selling_book
    )  # exits the for loop and prints the row with the highest number of sales
    list_string = str(best_selling_book)
my_list = ast.literal_eval(list_string)
print(my_list[0])
data_to_write = [
    ['Book', 'Author', 'Sales in Millions'],
    [my_list[0], my_list[1], my_list[4]],
]
with open('Python 2 Intermediate\\bestseller_info.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data_to_write)
