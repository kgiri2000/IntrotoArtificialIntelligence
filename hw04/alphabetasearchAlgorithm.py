from __future__ import print_function
import random
from random import randrange
import copy
import time

def GetMoves(Player, Board):
    MoveList = []
    for i in range(1, NumRows + 1):
        for j in range(1, NumCols + 1):
            if Board[i][j] == Player:
                for m in range(-1, 2):
                    for n in range(-1, 2):
                        if abs(m) != abs(n):
                            if Board[i + m][j + n] == Empty:
                                MoveList.append([i, j, i + m, j + n])

    return MoveList


def GetHumanMove(Player, Board):
    MoveList = GetMoves(Player, Board)
    Move = None

    while True:
        FromRow, FromCol, ToRow, ToCol = map(int, input('Input your move (FromRow, FromCol, ToRow, ToCol): ').split(' '))

        ValidMove = False
        if not ValidMove:
            for move in MoveList:
                if move == [FromRow, FromCol, ToRow, ToCol]:
                    ValidMove = True
                    Move = move

        if ValidMove:
            break

        print('Invalid move.  ')

    return Move


def ApplyMove(Board, Move):
    FromRow, FromCol, ToRow, ToCol = Move
    newBoard = copy.deepcopy(Board)
    newBoard[ToRow][ToCol] = newBoard[FromRow][FromCol]
    newBoard[FromRow][FromCol] = Empty
    return newBoard


def InitBoard(Board):
    for i in range(0, BoardRows + 1):
        for j in range(0, BoardCols + 1):
            Board[i][j] = OutOfBounds

    for i in range(1, NumRows + 1):
        for j in range(1, NumCols + 1):
            Board[i][j] = Empty

    for j in range(1, NumCols + 1):
        if odd(j):
            Board[1][j] = x
            Board[NumRows][j] = o
        else:
            Board[1][j] = o
            Board[NumRows][j] = x


def odd(n):
    return n % 2 == 1


def ShowBoard(Board):
    print("")
    row_divider = "+" + "-" * (NumCols * 4 - 1) + "+"
    print(row_divider)

    for i in range(1, NumRows + 1):
        for j in range(1, NumCols + 1):
            if Board[i][j] == x:
                print('| X ', end="")
            elif Board[i][j] == o:
                print('| O ', end="")
            elif Board[i][j] == Empty:
                print('|   ', end="")
        print('|')
        print(row_divider)

    print("")

def Win(Player, Board):
    # Check for a win in rows
    for i in range(1, NumRows + 1):
        for j in range(1, NumCols - 1):
            if Board[i][j] == Board[i][j + 1] == Board[i][j + 2] == Player:
                return True

    # Check for a win in columns
    for j in range(1, NumCols + 1):
        for i in range(1, NumRows - 1):
            if Board[i][j] == Board[i + 1][j] == Board[i + 2][j] == Player:
                return True

    # Check for a win in diagonals (top-left to bottom-right)
    for i in range(1, NumRows - 1):
        for j in range(1, NumCols - 1):
            if Board[i][j] == Board[i + 1][j + 1] == Board[i + 2][j + 2] == Player:
                return True

    # Check for a win in diagonals (top-right to bottom-left)
    for i in range(1, NumRows - 1):
        for j in range(3, NumCols + 1):
            if Board[i][j] == Board[i + 1][j - 1] == Board[i + 2][j - 2] == Player:
                return True

    return False

def GetComputerMove(Player, Board):
    _, bmove = max_value(Player, Board, -infinity, infinity, 0)
    return bmove

#Using the algorithm of alpha-beta pruning
def max_value(Player, Board, alpha, beta, depth):
    global states_with_pruning 
    states_with_pruning += 1
    if is_terminal(Player, Board, depth):
        return kgiri_h(Player, Board), None

    v = -infinity
    bmove = None

    for move in GetMoves(Player, Board):
        new_board = ApplyMove(Board, move)
        min_val, _ = min_value(Player, new_board, alpha, beta, depth + 1)

        if min_val > v:
            v = min_val
            bmove = move
        if v >= beta:
            return v, bmove

        alpha = max(alpha, v)

    return v, bmove


def min_value(Player, Board, alpha, beta, depth):
    global states_with_pruning 
    states_with_pruning += 1
    if is_terminal(Player, Board, depth):
        return kgiri_h(Player, Board),None

    v = infinity
    bmove = None

    for move in GetMoves(Player, Board):
        new_board = ApplyMove(Board, move)
        max_val, _ = max_value(-Player, new_board, alpha, beta, depth + 1)
        if max_val < v:
            v = max_val
            bmove = move
        if v <= alpha:
            return v, bmove
        beta = min(beta, v)
    
    return v, bmove


# Checking terminal states
def is_terminal(Player, Board, depth):
    if depth >= MaxDepth or Win(Player, Board) or Win(-Player, Board):
        return True
    else:
        return False



def kgiri_h(Player, Board):
    # Evaluate the board based on the number of two-in-a-row, three-in-a-row, and potential wins
    score = 0

    # Check rows and columns
    for i in range(1, NumRows + 1):
        for j in range(1, NumCols + 1):
            # Check rows
            if Board[i][j] == Player:
                score += 1
            elif Board[i][j] == -Player:
                score -= 1

            # Check columns
            if Board[j][i] == Player:
                score += 1
            elif Board[j][i] == -Player:
                score -= 1

    # Check diagonals
    for i in range(1, NumRows + 1):
        if Board[i][i] == Player:
            score += 1
        elif Board[i][i] == -Player:
            score -= 1

        if Board[i][NumCols - i + 1] == Player:
            score += 1
        elif Board[i][NumCols - i + 1] == -Player:
            score -= 1

    return score


if __name__ == "__main__":
    start_time = 0
    end_time = 0
    depth_achieved = 0
    states_with_pruning = 0

    x = -1
    o = 1
    Empty = 0
    OutOfBounds = 2
    NumRows = 5
    BoardRows = NumRows + 1
    NumCols = 4
    BoardCols = NumCols + 1
    MaxMoves = 4 * NumCols
    NumInPackedBoard = 4 * (BoardRows + 1) * (BoardCols + 1)
    infinity = 10000  # Value of a winning board
    MaxDepth = 4
    Board = [[0 for col in range(BoardCols + 1)] for row in range(BoardRows + 1)]
    print("\nThe squares of the board are numbered by row and column, with '1 1' ")
    print("in the upper left corner, '1 2' directly to the right of '1 1', etc.")
    print("")
    print("Moves are of the form 'i j m n', where (i,j) is a square occupied")
    print("by your piece, and (m,n) is the square to which you move it.")
    print("")
    print("You move the 'X' pieces.\n")

    InitBoard(Board)
    ShowBoard(Board)

    MoveList = GetMoves(x, Board)
    print(MoveList)
    MoveList = GetMoves(o, Board)
    print(MoveList)

    torf = False

    t_computer = 0
    
    while not torf:
       
        Move = GetHumanMove(x, Board)
        depth_achieved += 1
        Board = ApplyMove(Board, Move)
        ShowBoard(Board)
        torf = Win(x, Board)
        if torf:
            print("Player Wins!!")
            break
        
        t_computer += (end_time- start_time)
        start_time = time.time()
        Move = GetComputerMove(o, Board)
        depth_achieved +=1
        Board = ApplyMove(Board, Move)
        ShowBoard(Board)
        torf = Win(o, Board)
        if torf:
            print("Computer Wins")
            break
        end_time = time.time()
        t_computer += (end_time - start_time)
    if not torf:

        print("Draw")

    end_time = time.time()
    print("Time taken by Computer:", t_computer)
    print("States with pruning: ", states_with_pruning)
    print("Depth Achieved: " , depth_achieved)
