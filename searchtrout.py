import twl
#dfs from starting point using twl.children()
LETTER_SCORES = {'?': 0, 'A': 1, 'E': 1, 'I': 1, 'O': 1, 'N': 1, 'R': 1, 'T': 1, 'L': 1, 'S': 1, 'U': 1, 'D': 2, 'G': 2, 'B': 3, 'C': 3, 'M': 3, 'P': 3, 'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4, 'K': 5, 'J': 8, 'X': 8, 'Q': 10, 'Z': 10}
ALL_BONUS_SQUARES = {(0, 0): 'TW', (0, 7): 'TW', (0, 14): 'TW', (7, 0): 'TW', (7, 14): 'TW', (14, 0): 'TW', (14, 7): 'TW', (14, 14): 'TW', (1, 1): 'DW', (2, 2): 'DW', (3, 3): 'DW', (4, 4): 'DW', (1, 13): 'DW', (2, 12): 'DW', (3, 11): 'DW', (4, 10): 'DW', (10, 4): 'DW', (11, 3): 'DW', (12, 2): 'DW', (13, 1): 'DW', (13, 13): 'DW', (12, 12): 'DW', (11, 11): 'DW', (10, 10): 'DW', (7, 7): 'DW', (1, 5): 'TL', (1, 9): 'TL', (5, 1): 'TL', (5, 5): 'TL', (5, 9): 'TL', (5, 13): 'TL', (9, 1): 'TL', (9, 5): 'TL', (9, 9): 'TL', (9, 13): 'TL', (13, 5): 'TL', (13, 9): 'TL', (2, 6): 'TL', (2, 8): 'TL', (6, 2): 'TL', (6, 6): 'TL', (6, 8): 'TL', (6, 12): 'TL', (8, 2): 'TL', (8, 6): 'TL', (8, 8): 'TL', (8, 12): 'TL', (12, 6): 'TL', (12, 8): 'TL', (0, 3): 'DL', (0, 11): 'DL', (2, 0): 'DL', (2, 7): 'DL', (2, 14): 'DL', (3, 2): 'DL', (3, 6): 'DL', (3, 8): 'DL', (3, 12): 'DL', (6, 3): 'DL', (6, 7): 'DL', (6, 11): 'DL', (7, 3): 'DL', (7, 11): 'DL', (8, 3): 'DL', (8, 7): 'DL', (8, 11): 'DL', (11, 2): 'DL', (11, 6): 'DL', (11, 8): 'DL', (11, 12): 'DL', (12, 0): 'DL', (12, 7): 'DL', (12, 14): 'DL', (14, 3): 'DL', (14, 11): 'DL'}
def dfs(prefix, row, col, dir, points_so_far, already_connected, board, original_rack_len, rack_left, blanks_used): #also, mult_so_far
    if board[row][col]:
        if dir == 'H':
            return dfs(prefix+board[row][col].lower(), row, col+1, dir, points_so_far+(LETTER_SCORES[board[row][col]] if board[row][col] == board[row][col].upper() else 0), True, board, original_rack_len, rack_left, blanks_used)
        else:
            return dfs(prefix + board[row][col].lower(), row + 1, col, dir, points_so_far + (LETTER_SCORES[board[row][col]] if board[row][col] == board[row][col].upper() else 0), True, board, original_rack_len, rack_left, blanks_used)
    possible_next = list(twl.children(prefix))
    all_possibilities = []
    for i in possible_next:
        if i == '$':
            if len(rack_left) != original_rack_len:
                all_possibilities.append((prefix, points_so_far, blanks_used))
        elif i.upper() not in rack_left:
            continue
        elif dir == 'H':
            l_b = row
            while l_b >= 1 and board[l_b-1][col]:
                l_b -= 1
            u_b = row
            while u_b <= 13 and board[u_b+1][col]:
                u_b += 1
            if l_b != row or u_b != row:
                crossword_score = 0
                crossword = ''
                for r in range(l_b, u_b+1):
                    crossword_score += LETTER_SCORES[board[r][col]] if board[r][col] == board[r][col].upper() else 0
                    crossword += board[r][col].lower()
                if not twl.check(crossword):
                    continue
                already_connected = True
                points_so_far += crossword_score
            rack_copy = rack_left[:]
            rack_copy.remove(i.upper())
            all_possibilities += dfs(prefix+i, row, col+1, dir, points_so_far+LETTER_SCORES[i.upper()], already_connected, board, original_rack_len, rack_copy, blanks_used)
        else:
            l_b = col
            while l_b >= 1 and board[row][l_b - 1]:
                l_b -= 1
            u_b = col
            while u_b <= 13 and board[row][u_b + 1]:
                u_b += 1
            if l_b != col or u_b != col:
                crossword_score = 0
                crossword = ''
                for c in range(l_b, u_b + 1):
                    crossword_score += LETTER_SCORES[board[row][c]] if board[row][c] == board[row][c].upper() else 0
                    crossword += board[row][c]
                if not twl.check(crossword):
                    continue
                already_connected = True
                points_so_far += crossword_score
            rack_copy = rack_left[:]
            rack_copy.remove(i.upper())
            all_possibilities += dfs(prefix + i, row + 1, col, dir, points_so_far+LETTER_SCORES[i.upper()], already_connected, board, original_rack_len, rack_copy, blanks_used)
    return all_possibilities

board = [['']*15 for i in range(15)]
board[7][7] = 'A'
board[8][7] = 'S'
print(dfs('', 7, 7, 'H', 0, False, board, 5, ['I', 'N', 'I', 'N', 'E'], []))