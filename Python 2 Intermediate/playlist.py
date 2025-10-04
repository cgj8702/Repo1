liked_songs = {
    'Bad Habits': 'Ed Sheeran',
    'I\'m Just Ken': 'Ryan Golsing',
    'Mastermind': 'Taylor Swift',
    'Uptown Funk': 'Mark Ronson ft. Bruno Mars',
    'Ghost': 'Justin Bieber',
}

# for i in liked_songs:
#  print(i, 'by', liked_songs[i])
# this is the way to print key,value pairs using i by itself btw

# return values for dictionaries are keys by default which makes this extra confusing !!!


def write_liked_songs_to_file(liked_songs, file_name):
    with open(file_name, 'w') as file:
        file.write('Liked Songs:\n')
        for song, artist in liked_songs.items():
            file.write(f' {song} by {artist}\n')


write_liked_songs_to_file(liked_songs, 'Python 2 Intermediate\\playlist.txt')
