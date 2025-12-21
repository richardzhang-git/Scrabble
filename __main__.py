board = [['.']*15 for i in range(15)]
def display():
    global board
    print('\n'.join([''.join(i) for i in board]))

while True:
    display()
    word = input("Word: ").upper()
    start_x, start_y = map(int, input("Location: ").split())
    direction = input("Dir: ")
    for i in range(len(word)):
        if direction == 'H':
            board[start_y][start_x+i] = word[i]
        else:
            board[start_y+i][start_x] = word[i]