import twl
import numpy as np
from collections import Counter
'''keep record of previous board and previous possible 1 branches
high score: 559'''
LETTER_SCORES = {'?': 0, 'A': 1, 'E': 1, 'I': 1, 'O': 1, 'N': 1, 'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1, 'D': 2, 'G': 2, 'B': 3, 'C': 3, 'M': 3, 'P': 3, 'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4, 'K': 5, 'J': 8, 'X': 8, 'Q': 10, 'Z': 10}
ALL_BONUS_SQUARES = {(0, 0): 'TW', (0, 7): 'TW', (0, 14): 'TW', (7, 0): 'TW', (7, 14): 'TW', (14, 0): 'TW', (14, 7): 'TW', (14, 14): 'TW', (1, 1): 'DW', (2, 2): 'DW', (3, 3): 'DW', (4, 4): 'DW', (1, 13): 'DW', (2, 12): 'DW', (3, 11): 'DW', (4, 10): 'DW', (10, 4): 'DW', (11, 3): 'DW', (12, 2): 'DW', (13, 1): 'DW', (13, 13): 'DW', (12, 12): 'DW', (11, 11): 'DW', (10, 10): 'DW', (7, 7): 'DW', (1, 5): 'TL', (1, 9): 'TL', (5, 1): 'TL', (5, 5): 'TL', (5, 9): 'TL', (5, 13): 'TL', (9, 1): 'TL', (9, 5): 'TL', (9, 9): 'TL', (9, 13): 'TL', (13, 5): 'TL', (13, 9): 'TL', (2, 6): 'TL', (2, 8): 'TL', (6, 2): 'TL', (6, 6): 'TL', (6, 8): 'TL', (6, 12): 'TL', (8, 2): 'TL', (8, 6): 'TL', (8, 8): 'TL', (8, 12): 'TL', (12, 6): 'TL', (12, 8): 'TL', (0, 3): 'DL', (0, 11): 'DL', (2, 0): 'DL', (2, 7): 'DL', (2, 14): 'DL', (3, 2): 'DL', (3, 6): 'DL', (3, 8): 'DL', (3, 12): 'DL', (6, 3): 'DL', (6, 7): 'DL', (6, 11): 'DL', (7, 3): 'DL', (7, 11): 'DL', (8, 3): 'DL', (8, 7): 'DL', (8, 11): 'DL', (11, 2): 'DL', (11, 6): 'DL', (11, 8): 'DL', (11, 12): 'DL', (12, 0): 'DL', (12, 7): 'DL', (12, 14): 'DL', (14, 3): 'DL', (14, 11): 'DL'}
board = [[["", None] for j in range(15)] for i in range(15)] #None = blank, L = left possible, R = right possible, U = up possible, D = down possible, LR, etc. with mixed = multiple possible N = none (blocked or used)
board_empty = True
possible_points = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}
possible_indexes = np.array([[-1, -1], ])
trout_score = 0
opp_score = 0 #update before board_state is uppercased

#preferences
BLANK_GREED = 0.5 #more positive, less willing to use
#TODO: strategy with max/min available tiles for opponent to play off of
#TODO: bridge towards bonus tiles
#TODO: save letters for big bingos?
#TODO: adapt based on score lead/loss
#TODO: spacial sense and moving towards open areas
#TODO: adding full word to get score of both word and anchor

def update_board(board_state, record_opp_score=False):
    global possible_indexes, opp_score, board
    new_points = []
    for i in range(15):
        for j in range(15):
            # print(i, j, board[i][j][0], board_state[i][j])
            if board_state[i][j] != "" and board_state[i][j] != board[i][j][0]:
                if record_opp_score:
                    new_points.append((i, j))
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
                        possible_points[board_state[possible_indexes[point][0]][possible_indexes[point][1]].upper()].remove(tuple(possible_indexes[point]))
                    else:
                        new_pos_i.append(possible_indexes[point])
                new_pos_i = np.array(new_pos_i)
                possible_indexes = new_pos_i.copy()
                if valid_placements:
                    possible_points[board_state[i][j].upper()].append((i, j))
                    possible_indexes = np.append(possible_indexes, [(i, j)], axis=0)
                board[i][j][0] = board_state[i][j]
                board[i][j][1] = valid_placements
    if record_opp_score and new_points:
        if len(new_points) > 1 and new_points[0][0] == new_points[1][0]:
            new_points.sort(key=lambda x: x[1])
            new_scores = []
            l_b = new_points[0][1]
            while l_b >= 1 and board_state[new_points[0][0]][l_b-1] != '':
                l_b -= 1
            u_b = new_points[-1][1]
            while u_b <= 13 and board_state[new_points[0][0]][u_b+1] != '':
                u_b += 1
            # print("bound", l_b, u_b)
            for i in range(l_b, u_b+1):
                if board_state[new_points[0][0]][i] != board_state[new_points[0][0]][i].upper():
                    new_scores.append(0)
                else:
                    new_scores.append(LETTER_SCORES[board_state[new_points[0][0]][i]])
            for p in new_points:
                if p in ALL_BONUS_SQUARES.keys():
                    if ALL_BONUS_SQUARES[p] == 'TL':
                        new_scores[p[1]-l_b] *= 3
                    elif ALL_BONUS_SQUARES[p] == 'DL':
                        new_scores[p[1] - l_b] *= 2
                    elif ALL_BONUS_SQUARES[p] == 'TW':
                        new_scores = [i*3 for i in new_scores]
                    else:
                        new_scores = [i*2 for i in new_scores]
            print(new_scores)
            print(sum(new_scores))
            opp_score += sum(new_scores)
            print(new_points)
            if len(new_points) == 7:
                opp_score += 50
        elif len(new_points) > 1:
            new_points.sort(key=lambda x: x[0])
            new_scores = []
            l_b = new_points[0][0]
            while l_b >= 1 and board_state[l_b-1][new_points[0][1]] != '':
                l_b -= 1
            u_b = new_points[-1][0]
            while u_b <= 13 and board_state[u_b+1][new_points[0][1]] != '':
                u_b += 1
            # print("bound", l_b, u_b)
            for i in range(l_b, u_b + 1):
                if board_state[i][new_points[0][1]] != board_state[i][new_points[0][1]].upper():
                    new_scores.append(0)
                else:
                    new_scores.append(LETTER_SCORES[board_state[i][new_points[0][1]]])
            for p in new_points:
                if p in ALL_BONUS_SQUARES.keys():
                    if ALL_BONUS_SQUARES[p] == 'TL':
                        new_scores[p[0] - l_b] *= 3
                    elif ALL_BONUS_SQUARES[p] == 'DL':
                        new_scores[p[0] - l_b] *= 2
                    elif ALL_BONUS_SQUARES[p] == 'TW':
                        new_scores = [i * 3 for i in new_scores]
                    else:
                        new_scores = [i * 2 for i in new_scores]
            print(new_scores)
            print(sum(new_scores))
            print(new_points)
            opp_score += sum(new_scores)
            if len(new_points) == 7:
                opp_score += 50
        else:
            point = new_points[0]
            if (point[0] <= 13 and board_state[point[0]+1][point[1]]) or (point[0] >= 1 and board_state[point[0]-1][point[1]]):
                l_b = point[0]
                u_b = point[0]
                while l_b >= 1 and board_state[l_b - 1][point[1]] != '':
                    l_b -= 1
                while u_b <= 13 and board_state[u_b + 1][point[1]] != '':
                    u_b += 1
                new_score = 0
                for i in range(l_b, u_b+1):
                    if board_state[i][point[1]] == board_state[i][point[1]].upper():
                        new_score += LETTER_SCORES[board_state[i][point[1]]]
                if point in ALL_BONUS_SQUARES.keys():
                    if ALL_BONUS_SQUARES[point] == 'TW':
                        new_score *= 3
                    elif ALL_BONUS_SQUARES[point] == 'DW':
                        new_score *= 2
                    elif ALL_BONUS_SQUARES[point] == 'TL':
                        new_score += LETTER_SCORES[board_state[point[0]][point[1]]]*2
                    else:
                        new_score += LETTER_SCORES[board_state[point[0]][point[1]]]
            else:
                l_b = point[1]
                u_b = point[1]
                while l_b >= 1 and board_state[point[0]][l_b-1] != '':
                    l_b -= 1
                while u_b <= 13 and board_state[point[0]][u_b+1] != '':
                    u_b += 1
                new_score = 0
                for i in range(l_b, u_b + 1):
                    if board_state[point[0]][i] == board_state[point[0]][i].upper():
                        new_score += LETTER_SCORES[board_state[point[0]][i]]
                if point in ALL_BONUS_SQUARES.keys():
                    if ALL_BONUS_SQUARES[point] == 'TW':
                        new_score *= 3
                    elif ALL_BONUS_SQUARES[point] == 'DW':
                        new_score *= 2
                    elif ALL_BONUS_SQUARES[point] == 'TL':
                        new_score += LETTER_SCORES[board_state[point[0]][point[1]]] * 2
                    else:
                        new_score += LETTER_SCORES[board_state[point[0]][point[1]]]
            opp_score += new_score
            print(new_score)
        # print(new_points)
        print('opp', opp_score)


def getMove(rack, board_state, bonus_squares):
    global board, board_empty, LETTER_SCORES, possible_points, possible_indexes, trout_score, opp_score
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
            offsets = []
            for i in potential:
                i = i.upper()
                rack_counter_copy = rack_counter.copy()
                blanks_index = []
                if has_blank:
                    v_score = []
                    for l in range(len(i)):
                        rack_counter_copy.subtract([i[l]])
                        if rack_counter_copy[i[l]] < 0:
                            v_score.append(0)
                            blanks_index.append(l)
                        else:
                            v_score.append(LETTER_SCORES[i[l]])
                else:
                    v_score = [LETTER_SCORES[l] for l in i]
                max_score = v_score.copy()
                offset = 0
                direction = "V"
                for j in range(len(i)):
                    temp_score = v_score.copy()
                    if j+1 < len(temp_score):
                        temp_score[j+1] *= 2
                    if j+5 < len(temp_score):
                        temp_score[j+5] *= 2
                    if j-1 >= 0:
                        temp_score[j-1] *= 2
                    if sum(temp_score) > sum(max_score):
                        max_score = temp_score
                        offset = j
                for j in range(len(i)):
                    temp_score = v_score.copy()
                    if j+4 < len(temp_score):
                        temp_score[j+4] *= 2
                    if j-4 >= 0:
                        temp_score[j-4] *= 2
                    if sum(temp_score) > sum(max_score):
                        max_score = temp_score
                        offset = j
                        direction = 'H'
                v_score = sum(max_score)
                scores.append(v_score + (50 if len(i) == 7 else 0))
                directions.append(direction)
                offsets.append(offset)
                blanks_used.append(blanks_index)
            potential = list(zip(potential, scores, directions, offsets, blanks_used))
            potential.sort(key=lambda x: x[1] - BLANK_GREED*len(x[4]))
            chosen_word = list(potential[-1][0].upper())
            for i in potential[-1][4]:
                chosen_word[i] = chosen_word[i].lower()
            chosen_word = "".join(chosen_word)
            trout_score += potential[-1][1]
            if potential[-1][2] == 'H':
                return [(7, 7+i-potential[-1][3], chosen_word[i]) for i in range(len(chosen_word))]
            return [(7+i-potential[-1][3], 7, chosen_word[i]) for i in range(len(chosen_word))]
        return []
    #actual algorithm here
    possible_letters = list()
    update_board(board_state, True)
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
                            score.append(0)
                            blanks_index.append(l)
                        else:
                            score.append(LETTER_SCORES[word[l]])
                else:
                    score = [LETTER_SCORES[l] for l in word]
                for anchor_row, anchor_col in possible_points[anchor]:
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
                                    score_copy = score.copy()
                                    for j in range(anchor_row-i, anchor_row-i+len(word)):
                                        if (j, anchor_col) not in bonus_squares.keys():
                                            continue
                                        if bonus_squares[(j, anchor_col)] == 'TW':
                                            score_copy = [_*3 for _ in score_copy]
                                        elif bonus_squares[(j, anchor_col)] == 'DW':
                                            score_copy = [_*2 for _ in score_copy]
                                        elif bonus_squares[(j, anchor_col)] == 'TL':
                                            score_copy[j-anchor_row+i] *= 3
                                        else:
                                            score_copy[j - anchor_row + i] *= 2
                                    potential_words_dupes.append(word)
                                    scores.append(sum(score_copy) + (50 if len(word) > 7 else 0))
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
                                    score_copy = score.copy()
                                    for j in range(anchor_col - i, anchor_col - i + len(word)):
                                        if (anchor_row, j) not in bonus_squares.keys():
                                            continue
                                        if bonus_squares[(anchor_row, j)] == 'TW':
                                            score_copy = [_ * 3 for _ in score_copy]
                                        elif bonus_squares[(anchor_row, j)] == 'DW':
                                            score_copy = [_ * 2 for _ in score_copy]
                                        elif bonus_squares[(anchor_row, j)] == 'TL':
                                            score_copy[j - anchor_col + i] *= 3
                                        else:
                                            score_copy[j - anchor_col + i] *= 2
                                    potential_words_dupes.append(word)
                                    scores.append(sum(score_copy) + (50 if len(word) > 7 else 0))
                                    anchor_pos.append((anchor_row, anchor_col))
                                    directions.append('H')
                                    positions.append((anchor_row, anchor_col-i))
                                    blanks_used.append(blanks_index)
        possible_all_anchors += list(zip(potential_words_dupes, scores, anchor_pos, directions, positions, blanks_used))
    possible_all_anchors.sort(key=lambda x: x[1] - BLANK_GREED*len(x[5]), reverse=True)
    if len(possible_all_anchors):
        chosen_word = list(possible_all_anchors[0][0])
        trout_score += possible_all_anchors[0][1]
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
        for i in chosen_word:
            board_state[i[0]][i[1]] = i[2]
        update_board(board_state)
        #only return placed letters, not whole word
        print(trout_score)
        return chosen_word
    return []
