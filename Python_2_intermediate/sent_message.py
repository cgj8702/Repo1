file_path = 'Python 2 Intermediate\\sent_message.txt'
secret_message = 'This is a secret message lol'
unsent_message = 'This message has been unsent'

with open(file_path, 'w') as file:
    file.write(secret_message)

with open(file_path, 'r+') as file:
    file.read()
    file.seek(0)
    file.truncate(len(unsent_message))
    file.write(unsent_message)
    print(secret_message)
    print(unsent_message)
