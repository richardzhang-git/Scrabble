from idna import valid_label_length

import twl
import numpy as np
from collections import Counter
'''keep record of previous board and previous possible 1 branches
interface is broken for illegal moves
blanks can be outputted as capital and will then still be scored'''
LETTER_SCORES = {'?': 0, 'A': 1, 'E': 1, 'I': 1, 'O': 1, 'N': 1, 'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1, 'D': 2, 'G': 2, 'B': 3, 'C': 3, 'M': 3, 'P': 3, 'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4, 'K': 5, 'J': 8, 'X': 8, 'Q': 10, 'Z': 10}
board = [[["", None] for j in range(15)] for i in range(15)] #None = blank, L = left possible, R = right possible, U = up possible, D = down possible, LR, etc. with mixed = multiple possible N = none (blocked or used)
board_empty = True
possible_points = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}
possible_indexes = np.array([[-1, -1], ])

#preferences
BLANK_GREED = 0 #more negative, less willing to use
#TODO: doesn't have to start on center square, just go through it (optional)
def getMove(rack, board_state, bonus_squares):
    global board, board_empty, LETTER_SCORES, possible_points, possible_indexes
    for i in range(15):
        for j in range(15):
            board_state[i][j] = board_state[i][j].upper()
    rack_counter = Counter(rack)
    if board_empty: #check if first move
        for i in range(15):
            for j in range(15):
                if board_state[i][j] != "":
                    board_empty = False
                    break
            if not board_empty:
                break
    has_blank = '?' in rack
    scores = []
    directions = []
    blanks_used = []
    if board_empty: #first move
        potential = list(twl.anagram(''.join(rack).lower()))
        if potential:
            for i in potential:
                i = i.upper()
                rack_counter_copy = rack_counter.copy()
                blanks_index = []
                if has_blank:
                    v_score = []
                    for l in range(len(i)):
                        rack_counter_copy.subtract([i[l]])
                        if rack_counter_copy[i[l]] < 0:
                            v_score.append(BLANK_GREED)
                            blanks_index.append(l)
                        else:
                            v_score.append(LETTER_SCORES[i[l]])
                else:
                    v_score = [LETTER_SCORES[l] for l in i]
                h_score = v_score.copy()
                v_score[1] *= 2
                if len(v_score) >= 6:
                    v_score[5] *= 2
                if len(h_score) >= 5:
                    h_score[4] *= 2
                v_score = sum(v_score)
                h_score = sum(h_score)
                if v_score > h_score:
                    scores.append(v_score)
                    directions.append('V')
                else:
                    scores.append(h_score)
                    directions.append('H')
                blanks_used.append(blanks_index)
            potential = list(zip(potential, scores, directions, blanks_used))
            potential.sort(key=lambda x: x[1])
            chosen_word = list(potential[-1][0].upper())
            for i in potential[-1][3]:
                chosen_word[i] = chosen_word[i].lower()
            chosen_word = "".join(chosen_word)
            if potential[-1][2] == 'H':
                return [(7, 7+i, chosen_word[i]) for i in range(len(chosen_word))]
            return [(7+i, 7, chosen_word[i]) for i in range(len(chosen_word))]
        return []
    #actual algorithm here
    possible_letters = list()
    for i in range(15):
        for j in range(15):
            if board_state[i][j] != "" and board_state[i][j] != board[i][j][0]:
                valid_placements = ""
                up1 = i >= 1 and not board_state[i-1][j]
                up2 = i >= 2 and not board_state[i-2][j]
                down1 = i <= 13 and not board_state[i + 1][j]
                down2 = i <= 12 and not board_state[i + 2][j]
                if down1 and up1 and up2:
                    valid_placements += 'U'
                if up1 and down1 and down2:
                    valid_placements += 'D'
                left1 = j >= 1 and not board_state[i][j-1]
                left2 = j >= 2 and not board_state[i][j - 2]
                right1 = j <= 13 and not board_state[i][j+1]
                right2 = j <= 12 and not board_state[i][j+2]
                if right1 and left1 and left2:
                    valid_placements += 'L'
                if left1 and right1 and right2:
                    valid_placements += 'R'
                new_pos_i = [(-1, -1)] #first item is a buffer to set dimensions
                for point in range(1, len(possible_indexes)):
                    if 'U' in board[possible_indexes[point][0]][possible_indexes[point][1]][1] and j == possible_indexes[point][1] and -1 <= possible_indexes[point][0]-i <= 2:
                        board[possible_indexes[point][0]][possible_indexes[point][1]][1] = board[possible_indexes[point][0]][possible_indexes[point][1]][1].replace('U', '')
                    if 'D' in board[possible_indexes[point][0]][possible_indexes[point][1]][1] and j == possible_indexes[point][1] and -2 <= possible_indexes[point][0]-i <= 1:
                        board[possible_indexes[point][0]][possible_indexes[point][1]][1] = board[possible_indexes[point][0]][possible_indexes[point][1]][1].replace('D', '')
                    if 'L' in board[possible_indexes[point][0]][possible_indexes[point][1]][1] and i == possible_indexes[point][0] and -1 <= possible_indexes[point][1]-j <= 2:
                        board[possible_indexes[point][0]][possible_indexes[point][1]][1] = board[possible_indexes[point][0]][possible_indexes[point][1]][1].replace('L', '')
                    if 'R' in board[possible_indexes[point][0]][possible_indexes[point][1]][1] and i == possible_indexes[point][0] and -2 <= possible_indexes[point][1]-j <= 1:
                        board[possible_indexes[point][0]][possible_indexes[point][1]][1] = board[possible_indexes[point][0]][possible_indexes[point][1]][1].replace('R', '')
                    if not board[possible_indexes[point][0]][possible_indexes[point][1]][1]:
                        # print(possible_indexes[point])
                        # print(possible_points)
                        # print(possible_points[board_state[possible_indexes[point][0]][possible_indexes[point][1]]])
                        possible_points[board_state[possible_indexes[point][0]][possible_indexes[point][1]]].remove(tuple(possible_indexes[point]))
                    else:
                        new_pos_i.append(possible_indexes[point])
                new_pos_i = np.array(new_pos_i)
                possible_indexes = new_pos_i.copy()
                if valid_placements:
                    possible_points[board_state[i][j]].append((i, j))
                    possible_indexes = np.append(possible_indexes, [(i, j)], axis=0)
                board[i][j][0] = board_state[i][j]
                board[i][j][1] = valid_placements
    for i in possible_points.keys():
        if possible_points[i]:
            possible_letters.append(i)
    possible_all_anchors = []
    for anchor in list(possible_letters):
        potential = list(twl.anagram((''.join(rack) + anchor).lower()))
        potential_words_dupes = []
        scores = []
        anchor_pos = []
        directions = []
        positions = []
        blanks_used = []
        for word in potential:
            word = word.upper()
            if anchor in word:
                rack_counter_copy = rack_counter.copy()
                rack_counter_copy.update([anchor])
                blanks_index = []
                if has_blank:
                    score = []
                    for l in range(len(word)):
                        rack_counter_copy.subtract([word[l]])
                        if rack_counter_copy[word[l]] < 0:
                            score.append(BLANK_GREED)
                            blanks_index.append(l)
                        else:
                            score.append(LETTER_SCORES[word[l]])
                else:
                    score = [LETTER_SCORES[l] for l in word]
                for anchor_row, anchor_col in possible_points[anchor]: #TODO: implement special tiles
                    for i in range(len(word)):
                        if word[i] == anchor:
                            if 'U' in board[anchor_row][anchor_col][1] or 'D' in board[anchor_row][anchor_col][1]:
                                valid = not (anchor_row-i < 0 or anchor_row-i+len(word)-1 >= 15)
                                if valid:
                                    for j in range(max(0, anchor_row-i-1), min(15, anchor_row-i+len(word)+1)):
                                        for k in range(max(0, anchor_col-1), min(15, anchor_col+2)):
                                            if (j == anchor_row-i-1 or j == anchor_row-i+len(word)) and (k == anchor_col-1 or k == anchor_col + 1):
                                                continue
                                            if j != anchor_row and board[j][k][0]:
                                                valid = False
                                                break
                                        if not valid:
                                            break
                                if valid:
                                    potential_words_dupes.append(word)
                                    scores.append(sum(score))
                                    anchor_pos.append((anchor_row, anchor_col))
                                    directions.append('V')
                                    positions.append((anchor_row-i, anchor_col))
                                    blanks_used.append(blanks_index)
                            if 'L' in board[anchor_row][anchor_col][1] or 'R' in board[anchor_row][anchor_col][1]:
                                valid = not (anchor_col-i < 0 or anchor_col-i+len(word)-1 >= 15)
                                if valid:
                                    for j in range(max(0, anchor_col-i-1), min(15, anchor_col-i+len(word)+1)):
                                        for k in range(max(0, anchor_row-1), min(15, anchor_row+2)):
                                            if (j == anchor_col-i-1 or j == anchor_col-i+len(word)) and (k == anchor_row-1 or k == anchor_row + 1):
                                                continue
                                            if j != anchor_col and board[k][j][0]:
                                                valid = False
                                                break
                                        if not valid:
                                            break
                                if valid:
                                    potential_words_dupes.append(word)
                                    scores.append(sum(score))
                                    anchor_pos.append((anchor_row, anchor_col))
                                    directions.append('H')
                                    positions.append((anchor_row, anchor_col-i))
                                    blanks_used.append(blanks_index)
        possible_all_anchors += list(zip(potential_words_dupes, scores, anchor_pos, directions, positions, blanks_used))
    possible_all_anchors.sort(key=lambda x: x[1], reverse=True)
    if len(possible_all_anchors):
        print(possible_all_anchors[0])
        chosen_word = list(possible_all_anchors[0][0])
        for i in possible_all_anchors[0][5]:
            chosen_word[i] = chosen_word[i].lower()
        if possible_all_anchors[0][3] == 'H':
            row_cords = [possible_all_anchors[0][4][0]] * len(chosen_word)
            col_cords = [possible_all_anchors[0][4][1] + i for i in range(len(chosen_word))]
            chosen_word = list(zip(row_cords, col_cords, chosen_word))
            chosen_word.pop(possible_all_anchors[0][2][1]-possible_all_anchors[0][4][1])
        else:
            row_cords = [possible_all_anchors[0][4][0] + i for i in range(len(chosen_word))]
            col_cords = [possible_all_anchors[0][4][1]] * len(chosen_word)
            chosen_word = list(zip(row_cords, col_cords, chosen_word))
            chosen_word.pop(possible_all_anchors[0][2][0] - possible_all_anchors[0][4][0])
        #only return placed letters, not whole word
        return chosen_word
    return []



# import string
# import random
# rack = [random.choice(string.ascii_uppercase + '?') for i in range(7)]
# print(rack)
# test_board = [['']*15 for i in range(15)]
# test_board[7][7] = "E"
# test_board[7][8] = "X"
# test_board[7][9] = "E"
# test_board[7][10] = "S"
# test_board[8][3] = "B"
# test_board[8][4] = "O"
# test_board[8][5] = "R"
# test_board[8][6] = "A"
# print(getMove(rack, test_board, {}))