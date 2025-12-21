import twl
import numpy as np
'''keep record of previous board and previous possible 1 branches'''
LETTER_SCORES = {'?': 0, 'A': 1, 'E': 1, 'I': 1, 'O': 1, 'N': 1, 'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1, 'D': 2, 'G': 2, 'B': 3, 'C': 3, 'M': 3, 'P': 3, 'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4, 'K': 5, 'J': 8, 'X': 8, 'Q': 10, 'Z': 10}
board = np.array([[""]*15 for i in range(15)])
board_empty = True
def getMove(rack, board_state, bonus_squares):
    global board, board_empty, LETTER_SCORES
    if board_empty: #check if first move
        for i in range(15):
            for j in range(15):
                if board[i][j] != "":
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

print(getMove(["A", "C", "T", "E", "S", "W", "B"], board, []))