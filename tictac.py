import random
import os
import cv2
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import copy as cp
from MediapipeHandGestureRecognition import MediapipeHandGestureRecognition as HandGesRec
from XO_fn_boardGen import *
from XO_fn_conditionCheck import *
from XO_fn_Minimax import minimax_algorithm
import keyboard

cap = cv2.VideoCapture(3)
HandGes = HandGesRec()

winner = "" # sk

# sk
def draw_XO(board, frame):
    for i in range(3):
        for j in range(3):
            if(board[i][j] == "O"):
                cv2.putText(frame, "O", org=(70 + 200 * j, 130 + 150 * i), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 4, color=(255, 0, 0), thickness = 3, lineType=cv2.LINE_4)
            elif(board[i][j] == "X"):
                cv2.putText(frame, "X", org=(70 + 200 * j, 130 + 150 * i), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 4, color=(0, 0, 255), thickness = 3, lineType=cv2.LINE_4)

    return frame


def computerDecision(board):
    global isBoardDisplayedC
    global winner # sk
    while (checkTie(board) == False) and (checkWin(board, 'X') == False):
        uboard = generate_cells(board)
        if isBoardDisplayedC == False:
            print("COM TURN")
            dispboard(board)
            print("In Game")
            isBoardDisplayedC = True
        # dispUboard(uboard)

        # TODO run minimax algorithm here
        computer_decision = minimax_algorithm(uboard)
        computer_decision = int(computer_decision)

        if checkCompatible(board, computer_decision, 'O') == True:
            if checkTie(board) == True:
                dispboard(board)
                winner = "tie" #sk
                print(scoreBoard)
                print("Tie game! Play again? (S), Quit? (Q)")
                while (1):
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    ret, frame = cap.read()
                    flipped_frame = cv2.flip(frame, 1)
                    HandGes.detect(flipped_frame)
                    annotated_frame = HandGes.visualize(flipped_frame)
                    cv2.putText(annotated_frame, "Tie Game!!", org=(200, 250), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 2, color=(0, 255, 0), thickness = 2, lineType=cv2.LINE_4)
                    cv2.imshow('annotated frame', annotated_frame)

                    key = cv2.waitKey(1)
                    if key == ord('q'):
                        cv2.destroyAllWindows()
                        HandGes.release()
                        cap.release()
                        exit()
                    elif key == ord('s'):
                        board = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]
                        isTryAgainDisplayedP = False
                        GameInitializer(board)
                    else:
                        continue

            elif checkWin(board, 'O') == True:
                dispboard(board)
                winner = "computer" #sk
                updateScore(scoreBoard, "computer")
                print(scoreBoard)
                print("The computer won! Play again? (S), Quit? (Q)")
                while (1):
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    ret, frame = cap.read()
                    flipped_frame = cv2.flip(frame, 1)
                    HandGes.detect(flipped_frame)
                    annotated_frame = HandGes.visualize(flipped_frame)
                    cv2.putText(annotated_frame, "Computer Win!!", org=(120, 250), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 2, color=(0, 255, 0), thickness = 2, lineType=cv2.LINE_4)
                    cv2.imshow('annotated frame', annotated_frame)
                
                    key = cv2.waitKey(1)
                    if key == ord('q'):
                        cv2.destroyAllWindows()
                        HandGes.release()
                        cap.release()
                        exit()
                    elif key == ord('s'):
                        board = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]
                        isTryAgainDisplayedP = False
                        GameInitializer(board)
                    else:
                        continue

            else:
                # if
                #    print("Please select an empty spot and try again.")
                playerDecision(board)
        else:
           isBoardDisplayedC = False
           computerDecision(board)

def playerDecision(board):
    global isBoardDisplayedP
    global isTryAgainDisplayedP
    global winner # sk
    while (checkTie(board) == False) and (checkWin(board, 'O') == False):
        if isBoardDisplayedP == False:
            dispboard(board)
            # print("P TURN")
            print("Your turn")
            isBoardDisplayedP = True
        # player_decision = input("\n(The player's turn) Enter the empty position you want to place your 'X': ")
        # player_decision = int(player_decision)

        while cap.isOpened():
            ret, frame = cap.read()
            flipped_frame = cv2.flip(frame, 1)

            HandGes.detect(flipped_frame)
            annotated_frame = HandGes.visualize(flipped_frame)

            try:
                if HandGes.num_detected_hands>0:
                    handX,handY = HandGes.get_normalized_landmark(0,5)[0],HandGes.get_normalized_landmark(0,5)[1]
                    # frame.shape[0] --> Y Axis
                    # frame.shape[1] --> X Axis

                    # Detecting Blocks by x to Y
                    if handX <= 1/3:
                        if handY <= 1/3:
                            player_decision = 0
                        elif handY > 1/3 and handY <= 2/3:
                            player_decision = 3
                        elif handY > 2/3:
                            player_decision = 6
                    elif handX > 1/3 and handX <= 2/3:
                        if handY <= 1/3:
                            player_decision = 1
                        elif handY > 1/3 and handY <= 2/3:
                            player_decision = 4
                        elif handY > 2/3:
                            player_decision = 7
                    elif handX > 2/3:
                        if handY <= 1/3:
                            player_decision = 2
                        elif handY > 1/3 and handY <= 2/3:
                            player_decision = 5
                        elif handY > 2/3:
                            player_decision = 8
                    if (HandGes.get_gesture(0) == "Closed_Fist"):
                        break
            except TypeError:
                pass

            # Row
            cv2.line(annotated_frame,(0,frame.shape[0]//3),(700,frame.shape[0]//3),(0,0,0),3)
            cv2.line(annotated_frame,(0,2 * frame.shape[0]//3),(700,2 * frame.shape[0]//3),(0,0,0),3)

            # Column
            cv2.line(annotated_frame,(frame.shape[1]//3,0),(frame.shape[1]//3,500),(0,0,0),3)
            cv2.line(annotated_frame,(2 * frame.shape[1]//3,0),(2 * frame.shape[1]//3,500),(0,0,0),3)

            # show XO
            annotated_frame = draw_XO(board, annotated_frame)

            # show the score sk
            cv2.putText(annotated_frame, "{:d}:{:d}".format(scoreBoard["computerScore"], scoreBoard["playerScore"]), org=(285, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color=(0, 255, 0), thickness = 2, lineType=cv2.LINE_4)
        
            cv2.imshow('annotated frame', annotated_frame)
            key = cv2.waitKey(1)&0xFF
            if key == ord('q'):
                break

        if checkCompatible(board, player_decision, 'X') == True:
            isBoardDisplayedP = False
            if checkTie(board) == True:
                dispboard(board)
                winner = "tie" # sk
                print(scoreBoard)
                print("Tie game! Play again? (S), Quit? (Q) ")
                while (1):
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    ret, frame = cap.read()
                    flipped_frame = cv2.flip(frame, 1)
                    HandGes.detect(flipped_frame)
                    annotated_frame = HandGes.visualize(flipped_frame)
                    cv2.putText(annotated_frame, "Tie Game!!", org=(200, 250), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 2, color=(0, 255, 0), thickness = 2, lineType=cv2.LINE_4)
                    cv2.imshow('annotated frame', annotated_frame)

                    key = cv2.waitKey(1)
                    if key == ord('q'):
                        cv2.destroyAllWindows()
                        HandGes.release()
                        cap.release()
                        exit()
                    elif key == ord('s'):
                        board = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]
                        isTryAgainDisplayedP = False
                        GameInitializer(board)
                    else:
                        continue

            elif checkWin(board, 'X') == True:
                dispboard(board)
                winner = "player" #sk
                updateScore(scoreBoard, "player")
                print(scoreBoard)
                print("The player won! Play again? (S), Quit? (Q)")
                while (1): 
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    ret, frame = cap.read()
                    flipped_frame = cv2.flip(frame, 1)
                    HandGes.detect(flipped_frame)
                    annotated_frame = HandGes.visualize(flipped_frame)
                    cv2.putText(annotated_frame, "Player Win!!", org=(170, 250), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 2, color=(0, 255, 0), thickness = 2, lineType=cv2.LINE_4)
                    cv2.imshow('annotated frame', annotated_frame)

                    key = cv2.waitKey(1)
                    if key == ord('q'):
                        cv2.destroyAllWindows()
                        HandGes.release()
                        cap.release()
                        exit()
                    elif key == ord('s'):
                        board = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]
                        isTryAgainDisplayedP = False
                        GameInitializer(board)
                    else:
                        continue

            else:
                isTryAgainDisplayedP = False
                computerDecision(board)
        else:
            if isTryAgainDisplayedP == False:
                isTryAgainDisplayedP = True
                print("Please select an empty spot and try again.")
            playerDecision(board)

def updateScore(SB, winner):
    if winner == "player":
        scoreBoard["playerScore"] += 1
    elif winner == "computer":
        scoreBoard["computerScore"] += 1
    return scoreBoard

def GameInitializer(board):
    # Set default value
    global isBoardDisplayedC
    global isBoardDisplayedP
    global isTryAgainDisplayedP
    global isFirstGame
    isTryAgainDisplayedP = False
    isBoardDisplayedC = False
    isBoardDisplayedP = False

    # choice = input("\nPress any key to start")
    if isFirstGame == True:
        print(scoreBoard)
        print("Press S to start")
        while(1):
            try:
                if keyboard.is_pressed('S'):
                    print("ゲームスタート！")
                    break
            except:
                break

    # startingSide = 0 # for testing purposes
    startingSide = randStart()
    if startingSide == 1:
        print("Player start first")
        isFirstGame = False
        playerDecision(board)
    elif startingSide == 0:
        print("Computer start first")
        isBoardDisplayedC = True
        isFirstGame = False
        computerDecision(board)
    else:
        print("something's wrong")



def main():
    global scoreBoard
    global isFirstGame
    scoreBoard = {
        "computerScore" : 0,
        "playerScore" : 0
    }
    # Board, which is updated
    init_board = [[0, 1, 2], 
              [3, 4, 5],
              [6, 7, 8]]
    isFirstGame = True
    GameInitializer(init_board) # Start game

main()