import os
import sys

# Board configuration constants
BOARD_SIZE = 19
WIN_STREAK = 5

# Derived constants
BOARD_LAST_INDEX = BOARD_SIZE - 1  # 18
WIN_STREAK_MINUS_ONE = WIN_STREAK - 1  # 4

def check_victory(board):
    diag_forward_counts = [0]*BOARD_SIZE
    diag_backward_counts = [0]*BOARD_SIZE
    vert_counts = [0]*BOARD_SIZE
    for i,row in zip(range(BOARD_SIZE), board):
        horizontal_count = 0
        diag_forward_counts_new = [0]*BOARD_SIZE
        for j,c in zip(range(BOARD_SIZE), row):
            if c=='0':
                if horizontal_count==WIN_STREAK:
                    return int(row[j-1]), i, j-WIN_STREAK
                horizontal_count=0
                if j!=0 and diag_forward_counts[j-1]==WIN_STREAK:
                    return int(board[i-1][j-1]), i-WIN_STREAK, j-WIN_STREAK
                diag_forward_counts_new[j]=0
                if vert_counts[j]==WIN_STREAK:
                    return int(board[i-1][j]), i-WIN_STREAK, j
                vert_counts[j]=0
                if j!=BOARD_LAST_INDEX and diag_backward_counts[j+1]==WIN_STREAK:
                    return int(board[i-1][j+1]), i-1, j+1
                diag_backward_counts[j]=0
            else:
                if j==0:
                    horizontal_count=1
                elif row[j-1]!=c:
                    if horizontal_count==WIN_STREAK:
                        return int(row[j-1]), i, j-WIN_STREAK
                    horizontal_count=1
                else:
                    horizontal_count+=1
                    if j==BOARD_LAST_INDEX and horizontal_count==WIN_STREAK:
                        return int(c), i, BOARD_LAST_INDEX-WIN_STREAK_MINUS_ONE
                if j==0 or i==0:
                    diag_forward_counts_new[j]=1
                elif board[i-1][j-1]!=c:
                    if diag_forward_counts[j-1]==WIN_STREAK:
                        return int(board[i-1][j-1]), i-WIN_STREAK, j-WIN_STREAK
                    diag_forward_counts_new[j]=1
                else:
                    diag_forward_counts_new[j]=diag_forward_counts[j-1]+1
                    if (j==BOARD_LAST_INDEX or i==BOARD_LAST_INDEX) and diag_forward_counts_new[j]==WIN_STREAK:
                        return int(c), i-WIN_STREAK_MINUS_ONE, j-WIN_STREAK_MINUS_ONE
                if i==0:
                    vert_counts[j]=1
                elif board[i-1][j]!=c:
                    if vert_counts[j]==WIN_STREAK:
                        return int(board[i-1][j]), i-WIN_STREAK, j
                    vert_counts[j]=1
                else:
                    vert_counts[j]+=1
                    if i==BOARD_LAST_INDEX and vert_counts[j]==WIN_STREAK:
                        return int(c), BOARD_LAST_INDEX-WIN_STREAK_MINUS_ONE, j
                if i==0 or j==BOARD_LAST_INDEX:
                    diag_backward_counts[j]=1
                elif board[i-1][j+1]!=c:
                    if diag_backward_counts[j+1]==WIN_STREAK:
                        return int(board[i-1][j+1]), i-1, j+1
                    diag_backward_counts[j]=1
                else:
                    diag_backward_counts[j]=diag_backward_counts[j+1]+1
                    if (i==BOARD_LAST_INDEX or j==0) and diag_backward_counts[j]==WIN_STREAK:
                        return int(c), i, j
        diag_forward_counts = diag_forward_counts_new
    return 0, None, None

if __name__=='__main__':
    filename = sys.argv[1] if len(sys.argv)>1 else 'test.txt'
    with open(filename, 'r') as f:
        test_n = int(f.readline())
        for _ in range(test_n):
            board = [f.readline().replace(' ', '')[:19] for _ in range(19)]
            result, row, col = check_victory(board)
            print(result)
            if result:
                print(row+1, col+1)
