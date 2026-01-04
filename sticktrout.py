import twl
from collections import Counter

def unpack(d):
    new_d = dict()
    for key in d.keys():
        value = d[key]
        for c in key:
            new_d[c.upper()] = value
    return new_d

LETTER_SCORES = {
    "aeionrtlsu": 1,
    "dg": 2,
    "bcmp": 3,
    "fhvwy": 4,
    'k': 5,
    "jx": 8,
    "qz": 10,
    "?": 0
}
LETTER_SCORES = unpack(LETTER_SCORES)

is_first_move = True

def compare(x):
    return x[1]

def dfs(row: int, col: int, dir: str, board: list, rack: list, bonus_squares: dict):
    if dir == 'H':
        if col >= 1 and board[row][col-1]:
            return None
    else:
        if row >= 1 and board[row-1][col]:
            return None
    visited = dict()
    result = list()
    connections_in_word = list()
    connections_from_crossword = list()
    blanks_used = list()
    placed_tile = False
    can_bingo = len(rack) == 7
    if board[row][col]:
        stack = [board[row][col].lower()]
    else:
        stack = list(twl.children(""))[::-1]
    stack = list(zip(stack, [0]*len(stack), [1]*len(stack), [0]*len(stack), [0]*len(stack)))
    word_so_far = ""
    score_so_far = 0
    mult_so_far = 1
    crossword_scores = 0
    while stack:
        new_letter = stack.pop()
        if new_letter == "POP CROSSWORD":
            crossword_scores -= connections_from_crossword.pop()
            continue
        elif new_letter == "POP PLACED":
            placed_tile = False
            continue
        score_so_far = new_letter[1]
        mult_so_far = new_letter[2]
        crossword_scores = new_letter[3]
        new_letter = new_letter[0]
        is_blank = False
        if word_so_far+new_letter in visited:
            continue
        else:
            visited[word_so_far+new_letter] = True
        if new_letter == '$':
            if placed_tile and (connections_in_word or connections_from_crossword):
                result.append((word_so_far, score_so_far*mult_so_far+crossword_scores+(50 if can_bingo and not rack else 0), connections_in_word[:], blanks_used[:]))
                # if can_bingo and not rack:
                #     print("BINGO!", word_so_far, row, col, dir)
            continue
        if new_letter == "POP":
            rack.append(word_so_far[-1].upper())
            word_so_far = word_so_far[:-1]
            continue
        elif new_letter == "POP CONNECT":
            connections_in_word.pop()
            word_so_far = word_so_far[:-1]
            continue
        elif new_letter == "POP BLANK":
            blanks_used.pop()
            word_so_far = word_so_far[:-1]
            rack.append('?')
            continue
        if dir == 'H' and col+len(word_so_far)+1 > 14:
            continue
        elif dir == 'V' and row+len(word_so_far)+1 > 14:
            continue
        word_so_far += new_letter
        if not placed_tile:
            if (dir == 'H' and not board[row][col+len(word_so_far)-1]) or (dir == 'V' and not board[row+len(word_so_far)-1][col]):
                placed_tile = True
                stack.append("POP PLACED")
        if dir == 'H' and board[row][col+len(word_so_far)-1]:
            stack.append(("POP CONNECT", score_so_far, mult_so_far, crossword_scores))
            connections_in_word.append(len(word_so_far)-1)
        elif dir == 'V' and board[row+len(word_so_far)-1][col]:
            stack.append(("POP CONNECT", score_so_far, mult_so_far, crossword_scores))
            connections_in_word.append(len(word_so_far)-1)
        else:
            if new_letter.upper() not in rack:
                if '?' in rack:
                    rack.remove('?')
                    blanks_used.append(len(word_so_far)-1)
                    stack.append(("POP BLANK", score_so_far, mult_so_far, crossword_scores))
                    is_blank = True
                else:
                    word_so_far = word_so_far[:-1]
                    continue
            else:
                rack.remove(new_letter.upper())
                stack.append(("POP", score_so_far, mult_so_far, crossword_scores))
        #add score here
        if dir == 'H':
            if board[row][col+len(word_so_far)-1] == new_letter.upper():
                score_so_far += LETTER_SCORES[new_letter.upper()]
            elif not board[row][col+len(word_so_far)-1]:
                coords = (row, col+len(word_so_far)-1)
                if not is_blank:
                    score_so_far += LETTER_SCORES[new_letter.upper()]
                if coords in bonus_squares.keys():
                    if bonus_squares[coords] == 'TW':
                        mult_so_far *= 3
                    elif bonus_squares[coords] == 'DW':
                        mult_so_far *= 2
                    elif not is_blank and bonus_squares[coords] == 'TL':
                        score_so_far += LETTER_SCORES[new_letter.upper()]*2
                    elif not is_blank:
                        score_so_far += LETTER_SCORES[new_letter.upper()]
        else:
            if board[row+len(word_so_far)-1][col] == new_letter.upper():
                score_so_far += LETTER_SCORES[new_letter.upper()]
            elif not board[row+len(word_so_far)-1][col]:
                coords = (row+len(word_so_far)-1, col)
                if not is_blank:
                    score_so_far += LETTER_SCORES[new_letter.upper()]
                if coords in bonus_squares.keys():
                    if bonus_squares[coords] == 'TW':
                        mult_so_far *= 3
                    elif bonus_squares[coords] == 'DW':
                        mult_so_far *= 2
                    elif not is_blank and bonus_squares[coords] == 'TL':
                        score_so_far += LETTER_SCORES[new_letter.upper()]*2
                    elif not is_blank:
                        score_so_far += LETTER_SCORES[new_letter.upper()]
        #check crossword
        if dir == 'H' and not board[row][col+len(word_so_far)-1]:
            l_b = row
            while l_b >= 1 and board[l_b-1][col+len(word_so_far)-1]:
                l_b -= 1
            u_b = row
            while u_b <= 13 and board[u_b+1][col+len(word_so_far)-1]:
                u_b += 1
            if l_b != u_b:
                crossword = ''
                crossword_score = 0
                for i in range(l_b, u_b+1):
                    if i == row:
                        crossword += new_letter
                        if not is_blank:
                            crossword_score += LETTER_SCORES[new_letter.upper()]
                        continue
                    crossword += board[i][col+len(word_so_far)-1].lower()
                    crossword_score += LETTER_SCORES[board[i][col+len(word_so_far)-1]] if board[i][col+len(word_so_far)-1] == board[i][col+len(word_so_far)-1].upper() else 0
                coords = (row, col+len(word_so_far)-1)
                if coords in bonus_squares.keys():
                    if bonus_squares[coords] == 'TW':
                        crossword_score *= 3
                    elif bonus_squares[coords] == 'DW':
                        crossword_score *= 2
                    elif not is_blank and bonus_squares[coords] == 'TL':
                        crossword_score += LETTER_SCORES[new_letter.upper()]*2
                    elif not is_blank:
                        crossword_score += LETTER_SCORES[new_letter.upper()]
                if not twl.check(crossword):
                    continue
                stack.append("POP CROSSWORD")
                connections_from_crossword.append(crossword_score)
                crossword_scores += crossword_score
        elif dir == 'V' and not board[row + len(word_so_far) - 1][col]:
            l_b = col
            while l_b >= 1 and board[row + len(word_so_far) - 1][l_b - 1]:
                l_b -= 1
            u_b = col
            while u_b <= 13 and board[row + len(word_so_far) - 1][u_b + 1]:
                u_b += 1
            if l_b != u_b:
                crossword = ''
                crossword_score = 0
                for i in range(l_b, u_b + 1):
                    if i == col:
                        crossword += new_letter
                        if not is_blank:
                            crossword_score += LETTER_SCORES[new_letter.upper()]
                        continue
                    crossword += board[row + len(word_so_far) - 1][i].lower()
                    crossword_score += LETTER_SCORES[board[row + len(word_so_far) - 1][i]] if board[row + len(word_so_far) - 1][i] == board[row + len(word_so_far) - 1][i].upper() else 0
                coords = (row + len(word_so_far) - 1, col)
                if coords in bonus_squares.keys():
                    if bonus_squares[coords] == 'TW':
                        crossword_score *= 3
                    elif bonus_squares[coords] == 'DW':
                        crossword_score *= 2
                    elif not is_blank and bonus_squares[coords] == 'TL':
                        crossword_score += LETTER_SCORES[new_letter.upper()] * 2
                    elif not is_blank:
                        crossword_score += LETTER_SCORES[new_letter.upper()]
                if not twl.check(crossword):
                    continue
                stack.append("POP CROSSWORD")
                connections_from_crossword.append(crossword_score)
                crossword_scores += crossword_score
                # print(row, col, dir, word_so_far, crossword_score)
        #update stack
        if dir == 'H' and col+len(word_so_far) <= 14 and board[row][col+len(word_so_far)]:
            stack.append((board[row][col+len(word_so_far)].lower(), score_so_far, mult_so_far, crossword_scores))
        elif dir == 'V' and row+len(word_so_far) <= 14 and board[row+len(word_so_far)][col]:
            stack.append((board[row+len(word_so_far)][col].lower(), score_so_far, mult_so_far, crossword_scores))
        else:
            c = list(twl.children(word_so_far))
            for i in range(len(c)-1, -1, -1):
                next_letter = c[i]
                if word_so_far+next_letter not in visited:
                    if next_letter == '$' or next_letter.upper() in rack:
                        stack.append((next_letter, score_so_far, mult_so_far, crossword_scores))
                    else:
                        pass
    return max(result, key=compare) if result else None

def first_move(rack):
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
                if j + 1 < len(temp_score):
                    temp_score[j + 1] *= 2
                if j + 5 < len(temp_score):
                    temp_score[j + 5] *= 2
                if j - 1 >= 0:
                    temp_score[j - 1] *= 2
                if sum(temp_score) > sum(max_score):
                    max_score = temp_score
                    offset = j
            for j in range(len(i)):
                temp_score = v_score.copy()
                if j + 4 < len(temp_score):
                    temp_score[j + 4] *= 2
                if j - 4 >= 0:
                    temp_score[j - 4] *= 2
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
        potential.sort(key=lambda x: x[1])
        chosen_word = list(potential[-1][0].upper())
        for i in potential[-1][4]:
            chosen_word[i] = chosen_word[i].lower()
        chosen_word = "".join(chosen_word)
        # trout_score += potential[-1][1]
        if potential[-1][2] == 'H':
            return [(7, 7 + i - potential[-1][3], chosen_word[i]) for i in range(len(chosen_word))]
        return [(7 + i - potential[-1][3], 7, chosen_word[i]) for i in range(len(chosen_word))]
    return []

def getMove(rack, board_state, bonus_squares):
    global is_first_move, rack_weight
    if is_first_move and not ''.join([''.join(i) for i in board_state]):
        is_first_move = False
        return first_move(rack)
    possibilities = []
    for i in range(14):
        for j in range(14):
            horizontal_result = dfs(i, j, 'H', board_state, rack, bonus_squares)
            if horizontal_result is not None:
                possibilities.append((horizontal_result[0], horizontal_result[1], horizontal_result[2], horizontal_result[3], i, j, 'H'))
            vertical_result = dfs(i, j, 'V', board_state, rack, bonus_squares)
            if vertical_result is not None:
                possibilities.append((vertical_result[0], vertical_result[1], vertical_result[2], vertical_result[3], i, j, 'V'))
    if not possibilities:
        return []
    # print(possibilities)
    optimal = max(possibilities, key=compare)
    print(optimal)
    output = []
    for i in range(len(optimal[0])):
        if i not in optimal[2]:
            if optimal[6] == 'H':
                output.append((optimal[4], optimal[5]+i, optimal[0][i].upper()))
            else:
                output.append((optimal[4]+i, optimal[5], optimal[0][i].upper()))
    for i in optimal[3]:
        output[i] = (output[i][0], output[i][1], output[i][2].lower())
    return output