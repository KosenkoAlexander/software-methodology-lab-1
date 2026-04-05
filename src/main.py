import os
import sys

BOARD_SIZE = 19
WIN_STREAK = 5

def check_if_board_correct(board):
    if len(board)!=BOARD_SIZE:
        return False
    for row in board:
        if len(row)!=BOARD_SIZE:
            return False
        if len(set(row)-{'0', '1', '2'}):
            return False
    return True


def is_limit(i, j):
    return not(0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE)


def check_horizontal_victory(row):
    count = 0
    for c, j in zip(row, range(BOARD_SIZE)):
        if c=='0':
            if count==WIN_STREAK:
                return int(row[j-1]), j-WIN_STREAK
            count = 0
        elif j==0:
            count = 1
        elif c==row[j-1]:
            count+=1
        elif count==WIN_STREAK:
            return int(row[j-1]), j-WIN_STREAK
        else:
            count = 1
    if count == WIN_STREAK:
        return int(row[-1]), BOARD_SIZE-WIN_STREAK
    return 0, None



def check_victory(board):
    forward_diag_counts = [0]*BOARD_SIZE
    backward_diag_counts = [0]*BOARD_SIZE
    vert_counts = [0]*BOARD_SIZE
    for i,row in zip(range(BOARD_SIZE), board):
        horizontal_victory, horizontal_position = check_horizontal_victory(row)
        if horizontal_victory:
            return horizontal_victory, i, horizontal_position
        forward_diag_counts_new = [0]*BOARD_SIZE
        for j,c in zip(range(BOARD_SIZE), row):
            if c=='0':
                for old_counter, new_counter, direction in [(forward_diag_counts, forward_diag_counts_new, (1, 1)), (backward_diag_counts, backward_diag_counts, (1, -1)), (vert_counts, vert_counts, (1, 0))]:
                    if not is_limit(i-direction[0], j-direction[1]) and old_counter[j-direction[1]] == WIN_STREAK:
                        return int(board[i-direction[0]][j-direction[1]]), i-direction[0]*(WIN_STREAK if direction[1]>=0 else 1), j-direction[1]*(WIN_STREAK if direction[1]>=0 else 1)
                    new_counter[j] = 0
            else:
                for old_counter, new_counter, direction in [(forward_diag_counts, forward_diag_counts_new, (1, 1)), (backward_diag_counts, backward_diag_counts, (1, -1)), (vert_counts, vert_counts, (1, 0))]:
                    i_d = i-direction[0]
                    j_d = j-direction[1]
                    if is_limit(i_d, j_d):
                        new_counter[j]=1
                    elif board[i_d][j_d]!=c:
                        if old_counter[j_d] == WIN_STREAK:
                            return int(board[i_d][j_d]), i-direction[0]*(WIN_STREAK if direction[1]>=0 else 1), j-direction[1]*(WIN_STREAK if direction[1]>=0 else 1)
                        new_counter[j]=1
                    else:
                        new_counter[j]=old_counter[j_d]+1
                        if is_limit(i+direction[0], j+direction[1]) and new_counter[j]==WIN_STREAK:
                            return int(c), i-direction[0]*(WIN_STREAK-1) if direction[1]>=0 else i, j-direction[1]*(WIN_STREAK-1) if direction[1]>=0 else j
        forward_diag_counts = forward_diag_counts_new
    return 0, None, None

if __name__=='__main__':
    filename = sys.argv[1] if len(sys.argv)>1 else 'test.txt'
    with open(filename, 'r') as f:
        test_n = int(f.readline())
        for _ in range(test_n):
            board = [f.readline().replace(' ', '')[:BOARD_SIZE] for _ in range(BOARD_SIZE)]
            if not check_if_board_correct(board):
                print('Incorrect board!')
                break
            result, row, col = check_victory(board)
            print(result)
            if result:
                print(row+1, col+1)
