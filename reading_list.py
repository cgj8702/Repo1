# .append() method adds an item to the end of the list.
# .insert() method adds an item to a specific index.
# .remove() method removes an item from a list based on the value.
# .pop() method removes the item at a particular index.

books = [
    'Harry Potter',
    '1984',
    'The Fault in Our Stars',
    'The Mom Test',
    'Life in Code',
]

books.append('Pachinko')
books.remove('The Fault in Our Stars')
books.pop(1)
print(books)
