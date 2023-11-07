# XO Board/Condition Check fn.
import keyboard

def checkWin(board, sign):
    if checkHorizontal(board, sign) == True:
        return True
    if checkVertical(board, sign) == True:
        return True
    if checkDiagonal(board, sign) == True:
        return True
    return False

def checkTie(board):
    filled = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'O' or board[i][j] == 'X':
                filled += 1
    if filled == 9:
        return True
    return False

def checkDiagonal(board, sign):
    filled = 0
    if board[0][0] == sign or board[0][2] == sign:
        if board[0][0] == sign:
            for i in range(3):
                if board[i][i] == sign:
                    filled+=1
        elif board[0][2] == sign:
            for i in range(3):
                if board[2-i][i] == sign:
                    filled+=1
        if filled == 3:
            return True
    else:
        return False        

    #for i in range(len(board)):
    #    filled = 0
    #    if board[0][0] == sign:
    #        for j in range(len(board[i])):
    #            if board[j][j] == sign:
    #                filled += 1
    #    elif board[0][2] == sign:
    #        for j in range(len(board[i])):
    #            if board[0+j][2-j] == sign:
    #                filled += 1
    #if filled == 3:
    #    return True
    #return False

def checkHorizontal(board, sign): # NOTE BUGGY so fix it
    for i in range(0,3,1):
        if board[i][0] == sign:
            filled = 0
            for j in range(0,3,1):
                if board[i][j] == sign:
                    filled += 1
            if filled == 3:
                return True
    return False

    #for i in range(len(board)):
    #    if board[i][0] == sign:
    #        filled = 0
    #        for j in range(len(board[i])):
    #            if board[i][j] == sign:
    #                filled += 1
    #        if filled == 3:
    #            return True
    #return False

def checkVertical(board, sign):
    for i in range(len(board)):  
        if board[0][i] == sign:
            filled = 0
            for j in range(len(board[i])):
                if board[j][i] == sign:
                    filled += 1
            if filled == 3:
                return True
    return False

def checkCompatible(board, move, sign):
    i = 2
    if move <= 2:
        i = 0
    elif move >= 3 and move <= 5:
        i = 1
    
    loc = [i,(move-(i*3))]

    if board[loc[0]][loc[1]] == move:
        board[loc[0]][loc[1]] = sign
        return True
    else:
        return False
    
def resetGame():
    while(1):
        try:
            if keyboard.is_pressed('S'):
                print("ゲームレスタート！")
                return 0
            elif keyboard.is_pressed('Q'):
                print("Quit")
                return 1
        except:
                break
        
