import math

# def add(x, y):
#  answer = x + y
# return answer


# print(add(4.99, 9.99))  # total is 14.98


def add(a, b):
    answer = a + b
    return answer


def subtract(a, b):
    answer = a - b
    return answer


def multiply(a, b):
    answer = a * b
    return answer


def divide(a, b):
    answer = a / b
    return answer


def exp(a, b):
    answer = a**b
    return answer


# print(add(1, 2))
# print(subtract(1, 2))
# print(multiply(1, 2))
# print(divide(1, 2))
# print(exp(1, 2))


print('==================')
print('Area Calculator 📐')
print('==================')

shapes = ['1) Triangle', '2) Rectangle', '3) Square', '4) Circle', '5) Quit']

for i in shapes:
    print(i)


which_shape = int(input('Which shape: '))

if which_shape == 1:
    height = int(input('Height: '))
    base = int(input('Base: '))
    print('The area is', int((height * base) / 2))
elif which_shape == 2:
    length = int(input('Length: '))
    width = int(input('Width: '))
    print('The area is', int(length * width))
elif which_shape == 3:
    side = int(input('Side: '))
    print('The area is', int(side**2))
elif which_shape == 4:
    radius = int(input('Radius: '))
    print('The area is', int(math.pi * (radius**2)))
else:
    print('Goodbye.')
