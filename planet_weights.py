# Write code below 💖

earth_weight = float(input('Enter your weight: '))
planet = int(input('Enter the planet number: '))

if planet == 1:
    destination_weight = earth_weight * 0.38
    print('Mercury weight: ', destination_weight)
elif planet == 2:
    destination_weight = earth_weight * 0.91
    print('Venus weight: ', destination_weight)
elif planet == 3:
    destination_weight = earth_weight * 0.38
    print('Mars weight: ', destination_weight)
elif planet == 4:
    destination_weight = earth_weight * 2.53
    print('Jupiter weight: ', destination_weight)
elif planet == 5:
    destination_weight = earth_weight * 1.07
    print('Saturn weight: ', destination_weight)
elif planet == 6:
    destination_weight = earth_weight * 0.89
    print('Uranus weight: ', destination_weight)
elif planet == 7:
    destination_weight = earth_weight * 1.14
    print('Neptune weight: ', destination_weight)
else:
    print('Invalid planet number')
