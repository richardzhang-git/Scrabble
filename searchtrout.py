import twl
from collections import Counter

#dfs from starting point using twl.children()
LETTER_SCORES = {'?': 0, 'A': 1, 'E': 1, 'I': 1, 'O': 1, 'N': 1, 'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1, 'D': 2, 'G': 2, 'B': 3, 'C': 3, 'M': 3, 'P': 3, 'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4, 'K': 5, 'J': 8, 'X': 8, 'Q': 10, 'Z': 10}

#preferences
BLANK_GREED = 0.5

#TODO: problem with scoring
#TODO: implement blanks

trout_score = 0

def compare(arr):
    m = arr[0]
    for i in arr:
        if i[1] > m[1]:
            m = i
    return m

def dfs(prefix, row, col, dir, points_so_far, crossword_points, already_connected, board, original_rack_len, rack_left, blanks_used, mult_so_far, bonus_squares): #also, mult_so_far
    global types
    if col > 14 or row > 14:
        if twl.check(prefix) and already_connected and len(rack_left) != original_rack_len:
            return [(prefix, points_so_far*mult_so_far+crossword_points+(50 if original_rack_len == 7 and not len(rack_left) else 0), blanks_used)]
        return []
    if board[row][col]:
        if dir == 'H':
            return dfs(prefix + board[row][col].lower(), row, col+1, dir, points_so_far+(LETTER_SCORES[board[row][col]] if board[row][col] == board[row][col].upper() else 0), crossword_points, True, board, original_rack_len, rack_left, blanks_used, mult_so_far, bonus_squares)
        else:
            return dfs(prefix + board[row][col].lower(), row + 1, col, dir, points_so_far + (LETTER_SCORES[board[row][col]] if board[row][col] == board[row][col].upper() else 0), crossword_points, True, board, original_rack_len, rack_left, blanks_used, mult_so_far, bonus_squares)
    if not len(rack_left):
        if twl.check(prefix) and already_connected:
            return [(prefix, points_so_far*mult_so_far+crossword_points+(50 if original_rack_len == 7 and not len(rack_left) else 0), blanks_used)]
        return []
    possible_next = list(twl.children(prefix))
    all_possibilities = []
    for i in possible_next:
        if prefix == 'sautoir':
            print(row, col, prefix, i)
        has_crossword = False
        if i == '$':
            if len(rack_left) != original_rack_len and already_connected:
                all_possibilities.append((prefix, points_so_far*mult_so_far+crossword_points+(50 if original_rack_len == 7 and not len(rack_left) else 0), blanks_used))
        elif i.upper() not in rack_left:
            if '?' in rack_left: #differentiate between h and v
                if dir == 'H':
                    l_b = row
                    while l_b >= 1 and board[l_b - 1][col]:
                        l_b -= 1
                    u_b = row
                    while u_b <= 13 and board[u_b + 1][col]:
                        u_b += 1
                    crossword_score = 0
                    crossword_mult = 1
                    if l_b != row or u_b != row:
                        crossword = ''
                        for r in range(l_b, u_b + 1):
                            if r == row:
                                if (row, col) in bonus_squares.keys():
                                    if bonus_squares[(row, col)] == 'TW':
                                        crossword_mult *= 3
                                    elif bonus_squares[(row, col)] == 'DW':
                                        crossword_mult *= 2
                                crossword += i
                                continue
                            crossword_score += LETTER_SCORES[board[r][col]] if board[r][col] == board[r][col].upper() else 0
                            crossword += board[r][col].lower()
                        if not twl.check(crossword):
                            continue
                        else:
                            has_crossword = True
                    rack_copy = rack_left[:]
                    rack_copy.remove('?')
                    new_score = points_so_far
                    new_crossword_score = crossword_points + crossword_score * crossword_mult
                    new_mult = mult_so_far
                    if (row, col) in bonus_squares.keys():
                        if bonus_squares[(row, col)] == 'TW':
                            new_mult *= 3
                        elif bonus_squares[(row, col)] == 'DW':
                            new_mult *= 2
                    all_possibilities += dfs(prefix + i, row, col + 1, dir, new_score, new_crossword_score, already_connected or has_crossword, board, original_rack_len, rack_copy, blanks_used + [len(prefix)], new_mult, bonus_squares)
                else:
                    l_b = col
                    while l_b >= 1 and board[row][l_b - 1]:
                        l_b -= 1
                    u_b = col
                    while u_b <= 13 and board[row][u_b + 1]:
                        u_b += 1
                    crossword_score = 0
                    crossword_mult = 1
                    if l_b != col or u_b != col:
                        crossword = ''
                        for c in range(l_b, u_b + 1):
                            if c == col:
                                if (row, col) in bonus_squares.keys():
                                    if bonus_squares[(row, col)] == 'TW':
                                        crossword_mult *= 3
                                    elif bonus_squares[(row, col)] == 'DW':
                                        crossword_mult *= 2
                                crossword += i
                                continue
                            crossword_score += LETTER_SCORES[board[row][c]] if board[row][c] == board[row][c].upper() else 0
                            crossword += board[row][c]
                        if not twl.check(crossword):
                            continue
                        else:
                            has_crossword = True
                    rack_copy = rack_left[:]
                    rack_copy.remove('?')
                    new_score = points_so_far
                    new_crossword_score = crossword_points + crossword_score * crossword_mult
                    new_mult = mult_so_far
                    if (row, col) in bonus_squares.keys():
                        if bonus_squares[(row, col)] == 'TW':
                            new_mult *= 3
                        elif bonus_squares[(row, col)] == 'DW':
                            new_mult *= 2
                    all_possibilities += dfs(prefix + i, row + 1, col, dir, new_score, new_crossword_score, already_connected or has_crossword, board, original_rack_len, rack_copy, blanks_used, new_mult, bonus_squares)
        elif dir == 'H':
            l_b = row
            while l_b >= 1 and board[l_b-1][col]:
                l_b -= 1
            u_b = row
            while u_b <= 13 and board[u_b+1][col]:
                u_b += 1
            crossword_score = 0
            crossword_mult = 1
            if l_b != row or u_b != row:
                crossword = ''
                for r in range(l_b, u_b+1):
                    if r == row:
                        crossword_score += LETTER_SCORES[i.upper()]
                        if (row, col) in bonus_squares.keys():
                            if bonus_squares[(row, col)] == 'TW':
                                crossword_mult *= 3
                            elif bonus_squares[(row, col)] == 'DW':
                                crossword_mult *= 2
                            elif bonus_squares[(row, col)] == 'TL':
                                crossword_score += 2*LETTER_SCORES[i.upper()]
                            else:
                                crossword_score += LETTER_SCORES[i.upper()]
                        crossword += i
                        continue
                    crossword_score += LETTER_SCORES[board[r][col]] if board[r][col] == board[r][col].upper() else 0
                    crossword += board[r][col].lower()
                if not twl.check(crossword):
                    continue
                else:
                    has_crossword = True
            rack_copy = rack_left[:]
            rack_copy.remove(i.upper())
            new_score = points_so_far+LETTER_SCORES[i.upper()]
            new_crossword_score = crossword_points + crossword_score*crossword_mult
            new_mult = mult_so_far
            if (row, col) in bonus_squares.keys():
                if bonus_squares[(row, col)] == 'TW':
                    new_mult *= 3
                elif bonus_squares[(row, col)] == 'DW':
                    new_mult *= 2
                elif bonus_squares[(row, col)] == 'TL':
                    new_score += 2*LETTER_SCORES[i.upper()]
                else:
                    new_score += LETTER_SCORES[i.upper()]
            all_possibilities += dfs(prefix+i, row, col+1, dir, new_score, new_crossword_score, already_connected or has_crossword, board, original_rack_len, rack_copy, blanks_used, new_mult, bonus_squares)
        else:
            l_b = col
            while l_b >= 1 and board[row][l_b - 1]:
                l_b -= 1
            u_b = col
            while u_b <= 13 and board[row][u_b + 1]:
                u_b += 1
            crossword_score = 0
            crossword_mult = 1
            if l_b != col or u_b != col:
                crossword = ''
                for c in range(l_b, u_b + 1):
                    if c == col:
                        crossword_score += LETTER_SCORES[i.upper()]
                        if (row, col) in bonus_squares.keys():
                            if bonus_squares[(row, col)] == 'TW':
                                crossword_mult *= 3
                            elif bonus_squares[(row, col)] == 'DW':
                                crossword_mult *= 2
                            elif bonus_squares[(row, col)] == 'TL':
                                crossword_score += 2*LETTER_SCORES[i.upper()]
                            else:
                                crossword_score += LETTER_SCORES[i.upper()]
                        crossword += i
                        continue
                    crossword_score += LETTER_SCORES[board[row][c]] if board[row][c] == board[row][c].upper() else 0
                    crossword += board[row][c]
                if not twl.check(crossword):
                    continue
                else:
                    has_crossword = True
            rack_copy = rack_left[:]
            rack_copy.remove(i.upper())
            new_score = points_so_far+LETTER_SCORES[i.upper()]
            new_crossword_score = crossword_points + crossword_score*crossword_mult
            new_mult = mult_so_far
            if (row, col) in bonus_squares.keys():
                if bonus_squares[(row, col)] == 'TW':
                    new_mult *= 3
                elif bonus_squares[(row, col)] == 'DW':
                    new_mult *= 2
                elif bonus_squares[(row, col)] == 'TL':
                    new_score += 2*LETTER_SCORES[i.upper()]
                else:
                    new_score += LETTER_SCORES[i.upper()]
            all_possibilities += dfs(prefix + i, row + 1, col, dir, new_score, new_crossword_score, already_connected or has_crossword, board, original_rack_len, rack_copy, blanks_used, new_mult, bonus_squares)
    if row == 10 and col == 1 and prefix == '':
        print(all_possibilities)
    # return [compare(all_possibilities)] if len(all_possibilities) else []
    return all_possibilities

def firstMove(rack, board_state, bonus_squares):
    rack_counter = Counter(rack)
    potential = list(twl.anagram(''.join(rack).lower()))
    has_blank = '?' in rack
    scores = []
    directions = []
    blanks_used = []
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
        # trout_score += potential[-1][1]
        if potential[-1][2] == 'H':
            return [(7, 7+i-potential[-1][3], chosen_word[i]) for i in range(len(chosen_word))]
        return [(7+i-potential[-1][3], 7, chosen_word[i]) for i in range(len(chosen_word))]
    return []

def getMove(rack, board_state, bonus_squares):
    global trout_score
    board_empty = True
    for i in range(15):
        for j in range(15):
            if board_state[i][j] != "":
                board_empty = False
                break
        if not board_empty:
            break
    if board_empty:
        return firstMove(rack, board_state, bonus_squares)
    possibilities = []
    for i in range(14):
        for j in range(14):
            if i == 0 or not board_state[i-1][j]:
                vertical_result = dfs('', i, j, 'V', 0, 0, False, board_state, len(rack), rack, [], 1, bonus_squares)
                for word_i in range(len(vertical_result)):
                    possibilities.append((vertical_result[word_i][0], vertical_result[word_i][1], vertical_result[word_i][2], i, j, 'V'))
            if j == 0 or not board_state[i][j-1]:
                horizontal_result = dfs('', i, j, 'H', 0, 0, False, board_state, len(rack), rack, [], 1, bonus_squares)
                for word_i in range(len(horizontal_result)):
                    possibilities.append((horizontal_result[word_i][0], horizontal_result[word_i][1], horizontal_result[word_i][2], i, j, 'H'))
    if not len(possibilities):
        return []
    print(possibilities)
    max_tuple = compare(possibilities)
    print(max_tuple)
    output = []
    for i in range(len(max_tuple[0])):
        if max_tuple[5] == 'H':
            if not board_state[max_tuple[3]][max_tuple[4]+i]:
                output.append((max_tuple[3], max_tuple[4]+i, max_tuple[0][i] if i in max_tuple[2] else max_tuple[0][i].upper()))
        else:
            if not board_state[max_tuple[3]+i][max_tuple[4]]:
                output.append((max_tuple[3]+i, max_tuple[4], max_tuple[0][i] if i in max_tuple[2] else max_tuple[0][i].upper()))
    print(output)
    trout_score += max_tuple[1]
    print(trout_score)
    return output
#
# board = [['']*15 for i in range(15)]
# board[7][7] = 'A'
# board[8][7] = 'S'
# print(dfs('', 7, 7, 'V', 0, False, board, 5, ['I', 'N', 'I', 'N', 'E'], []))