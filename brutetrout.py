import twl
from collections import Counter
ALL_WORDS = list(twl.anagram("???????????????"))
LETTER_SCORES = {'?': 0, 'A': 1, 'E': 1, 'I': 1, 'O': 1, 'N': 1, 'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1, 'D': 2, 'G': 2, 'B': 3, 'C': 3, 'M': 3, 'P': 3, 'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4, 'K': 5, 'J': 8, 'X': 8, 'Q': 10, 'Z': 10}

def check_word(word, row, col, dir, board, rack, bonus_squares):
    word = word.upper()
    rack_counter = Counter(rack)
    scores = []
    blanks = []
    if dir == 'H':
        if col >= 1 and board[row][col-1]:
            return -1
        if col <= 14-len(word) and board[row][col+len(word)]:
            return -1
        placeable = False
        for i in range(row-1, row+2):
            for j in range(col, col+len(word)):
                placeable = True
                break
            if placeable:
                break
        if not placeable:
            return -1
        for i in range(len(word)):
            if board[row][col+i] and board[row][col+i].upper() != word[i]:
                return -1
            elif board[row][col+i]:
                scores.append(LETTER_SCORES[board[row][col+i]] if board[row][col+i] == board[row][col+i].upper() else 0)
            else:
                if rack_counter[word[i]]:
                    rack_counter[word[i]] -= 1
                    scores.append(LETTER_SCORES[word[i]])
                    if (row, col+i) in bonus_squares.keys():
                        if bonus_squares[(row, col+i)] == 'TW':
                            scores = [i*3 for i in scores]
                        elif bonus_squares[(row, col+i)] == 'DW':
                            scores = [i*2 for i in scores]
                        elif bonus_squares[(row, col+i)] == 'TL':
                            scores[i] *= 3
                        else:
                            scores[i] *= 2
                elif rack_counter['?']:
                    rack_counter['?'] -= 1
                    scores.append(0)
                    blanks.append(i)
                    if (row, col+i) in bonus_squares.keys():
                        if bonus_squares[(row, col+i)] == 'TW':
                            scores = [i*3 for i in scores]
                        elif bonus_squares[(row, col+i)] == 'DW':
                            scores = [i*2 for i in scores]
                else:
                    return -1
    else:
        if row >= 1 and board[row-1][col]:
            return -1
        if row <= 14-len(word) and board[row+len(word)][col]:
            return -1
        placeable = False
        for i in range(col - 1, col + 2):
            for j in range(row, row + len(word)):
                placeable = True
                break
            if placeable:
                break
        if not placeable:
            return -1
        for i in range(len(word)):
            if board[row+i][col] and board[row+i][col].upper() != word[i]:
                return -1
            elif board[row+i][col]:
                scores.append(LETTER_SCORES[board[row+i][col]] if board[row+i][col] == board[row+i][col].upper() else 0)
            else:
                if rack_counter[word[i]]:
                    rack_counter[word[i]] -= 1
                    scores.append(LETTER_SCORES[word[i]])
                    if (row+i, col) in bonus_squares.keys():
                        if bonus_squares[(row+i, col)] == 'TW':
                            scores = [i*3 for i in scores]
                        elif bonus_squares[(row+i, col)] == 'DW':
                            scores = [i*2 for i in scores]
                        elif bonus_squares[(row+i, col)] == 'TL':
                            scores[i] *= 3
                        else:
                            scores[i] *= 2
                elif rack_counter['?']:
                    rack_counter['?'] -= 1
                    scores.append(0)
                    blanks.append(i)
                    if (row+i, col) in bonus_squares.keys():
                        if bonus_squares[(row+i, col)] == 'TW':
                            scores = [i*3 for i in scores]
                        elif bonus_squares[(row+i, col)] == 'DW':
                            scores = [i*2 for i in scores]
                else:
                    return -1
    return sum(scores), blanks

def get_move(rack, board_state, bonus_squares):
    pass

board = [['']*15 for i in range(15)]
board[7][7] = "A"
board[7][8] = "S"
for i in ALL_WORDS:
    for row in range(15):
        for col in range(15):
            result = check_word(i, row, col, 'V', board, ['C', 'N', 'O', 'P', 'Y'], {})
            if result != -1:
                print(i, result)