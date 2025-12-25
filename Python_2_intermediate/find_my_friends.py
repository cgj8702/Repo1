# Write code below 💖

me = (35.979309, -78.509323)
jon = (35.910259, -79.055473)
mal = (35.781300, -78.641678)
dad = (34.689529, -77.120552)


def distance(a):
    if a is me:
        my_lat = a[0]
        my_long = a[1]
        print('My latitude:', my_lat, 'My longitude:', my_long)
    else:
        var_lat = a[0]
        var_long = a[1]
        print('Friend\'s latitude:', var_lat, 'Friend\'s longitude:', var_long)


distance(me)
distance(jon)
distance(mal)
distance(dad)

friends = jon + mal + dad
print('Friend\'s lat/long tuple:', friends)
