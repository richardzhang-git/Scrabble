import twl
import numpy as np
'''keep record of previous board and previous possible 1 branches'''
LETTER_SCORES = {'?': 0, 'A': 1, 'E': 1, 'I': 1, 'O': 1, 'N': 1, 'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1, 'D': 2, 'G': 2, 'B': 3, 'C': 3, 'M': 3, 'P': 3, 'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4, 'K': 5, 'J': 8, 'X': 8, 'Q': 10, 'Z': 10}
board = np.array([[["", None] for j in range(15)] for i in range(15)]) #None = blank, L = left possible, R = right possible, U = up possible, D = down possible, LR, etc. with mixed = multiple possible N = none (blocked or used)
board_empty = True
possible_points = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}
possible_indexes = []
def getMove(rack, board_state, bonus_squares):
    global board, board_empty, LETTER_SCORES, possible_points
    if board_empty: #check if first move
        for i in range(15):
            for j in range(15):
                if board_state[i][j] != "":
                    board_empty = False
                    break
            if not board_empty:
                break
    if board_empty: #first move
        potential = list(twl.anagram(''.join(rack).lower()))
        if potential:
            scores = [sum([LETTER_SCORES[l.upper()] for l in i]) for i in potential]
            potential = list(zip(potential, scores))
            potential.sort(key=lambda x: x[1])
            chosen_word = potential[-1][0]
            return [(7, 7+i, chosen_word[i]) for i in range(len(chosen_word))]
        return []
    #actual algorithm here
    possible_letters = list()
    for i in range(15):
        for j in range(15):
            if board_state[i][j] != "" and board_state[i][j] != board[i][j][0]:
                for point in range(len(possible_indexes)):
                    if True:
                        pass #TODO: detect blocking other side
                possible_points[board_state[i][j]].append((i, j))
                possible_indexes.append((i, j))
    print(possible_points)
    for i in possible_points.keys():
        if possible_points[i]:
            possible_letters.append(i)
    print(possible_letters)
import string
import random
rack = [random.choice(string.ascii_uppercase) for i in range(8)]
print(rack)
test_board = [['']*15 for i in range(15)]
test_board[0][0] = "A"
test_board[0][1] = "L"
test_board[0][2] = "L"
print(getMove(rack, test_board, []))