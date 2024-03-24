def write_to_trip(text):
    with open('trip/notes.txt', 'w') as file:
        file.write(text + '\n')

def add_to_trip(text):
    with open('trip/notes.txt', 'a') as file:
        file.write(text + '\n')