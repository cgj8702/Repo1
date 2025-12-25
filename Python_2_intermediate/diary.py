file = open('Python 2 Intermediate\\diaries.txt', 'a')

file.write('First entry\n')
file.write('Second entry\n')
file.writelines(['line 1\n', 'line 2\n', 'line 3\n'])

file.close()

file = open('Python 2 Intermediate\\diaries.txt', mode='r')
content = file.read()
print(content)

with open('Python 2 Intermediate\\diaries.txt', 'r') as f:
    content = f.read
    print(content)

print('end of code')
