import os
import sys

def check_victory(board):
    diag_forward_counts = [0]*19
    diag_backward_counts = [0]*19
    vert_counts = [0]*19
    for i,row in zip(range(19), board):
        horizontal_count = 0
        diag_forward_counts_new = [0]*19
        for j,c in zip(range(19), row):
            if c=='0':
                if horizontal_count==5:
                    return int(row[j-1]), i, j-5
                horizontal_count=0
                if j!=0 and diag_forward_counts[j-1]==5:
                    return int(board[i-1][j-1]), i-5, j-5
                diag_forward_counts_new[j]=0
                if vert_counts[j]==5:
                    return int(board[i-1][j]), i-5, j
                vert_counts[j]=0
                if j!=18 and diag_backward_counts[j+1]==5:
                    return int(board[i-1][j+1]), i-1, j+1
                diag_backward_counts[j]=0
            else:
                if j==0:
                    horizontal_count=1
                elif row[j-1]!=c:
                    if horizontal_count==5:
                        return int(row[j-1]), i, j-5
                    horizontal_count=1
                else:
                    horizontal_count+=1
                    if j==18 and horizontal_count==5:
                        return int(c), i, 18-4
                if j==0 or i==0:
                    diag_forward_counts_new[j]=1
                elif board[i-1][j-1]!=c:
                    if diag_forward_counts[j-1]==5:
                        return int(board[i-1][j-1]), i-5, j-5
                    diag_forward_counts_new[j]=1
                else:
                    diag_forward_counts_new[j]=diag_forward_counts[j-1]+1
                    if (j==18 or i==18) and diag_forward_counts_new[j]==5:
                        return int(c), i-4, j-4
                if i==0:
                    vert_counts[j]=1
                elif board[i-1][j]!=c:
                    if vert_counts[j]==5:
                        return int(board[i-1][j]), i-5, j
                    vert_counts[j]=1
                else:
                    vert_counts[j]+=1
                    if i==18 and vert_counts[j]==5:
                        return int(c), 18-4, j
                if i==0 or j==18:
                    diag_backward_counts[j]=1
                elif board[i-1][j+1]!=c:
                    if diag_backward_counts[j+1]==5:
                        return int(board[i-1][j+1]), i-1, j+1
                    diag_backward_counts[j]=1
                else:
                    diag_backward_counts[j]=diag_backward_counts[j+1]+1
                    if (i==18 or j==0) and diag_backward_counts[j]==5:
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
