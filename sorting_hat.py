# Write code below 💖

gryff = 0
raven = 0
huff = 0
slyth = 0

print('Q1) Do you like Dawn or Dusk?')
print('1) Dawn')
print('2) Dusk')
q1 = int(input('Enter your answer (1-4): '))

if q1 == 1:
  gryff += 1; raven += 1
elif q1 == 2:
  huff += 1; raven += 1 
else:
  print('Wrong input.')

print('Q2) When I\'m dead, I want people to remember me as:')
print('1) The Good')
print('2) The Great')
print('3) The Wise')
print('4) The Bold')
q2 = int(input('Enter your answer (1-4): '))

if q2 == 1:
  huff += 2
elif q2 == 2:
  slyth += 2
elif q2 == 3:
    raven += 2
elif q2 == 4:
  gryff += 2
else: 
  print('Wrong input.')

print('Q3) Which kind of instrument most pleases your ear?')
print('1) The violin')
print('2) The trumpet')
print('3) The piano')
print('4) The drum')
q3 = int(input('Enter your answer (1-4): '))

if q3 == 1:
  slyth += 4
elif q3 == 2:
  huff += 4
elif q3 == 3:
  raven += 4
elif q3 == 4:
  gryff += 4
else:
  print('Wrong input.')

print('Gryffindor:', gryff)
print('Ravenclaw:', raven)
print('Hufflepuff:', huff)
print('Slytherin:', slyth)