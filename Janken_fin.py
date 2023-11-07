import random
import os
import cv2
import time
import math as m
from MediapipeHandGestureRecognition import MediapipeHandGestureRecognition as HandGesRec
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

# Key function definitions
def get_computer_choice():
    choices = ["rock", "paper", "scissors"]
    return random.choice(choices)

def updateScore(scoreBoard, winner):
    if winner == "Player":
        scoreBoard["playerScore"] += 1
    elif winner == "Computer":
        scoreBoard["computerScore"] += 1
    return scoreBoard

def determine_winner(user_choice, computer_choice, scoreBoard):
    if user_choice == computer_choice:
        winner = "None"
        #return "It's a tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        winner = "Player"
        #return "You win!"
    else:
        winner = "Computer"
        #return "Computer wins!"
    updateScore(scoreBoard, winner)
    return winner, scoreBoard

def result(user_choice, computer_choice, scoreBoard):
    print(f"You chose "+ user_choice)
    print(f"Computer chose {computer_choice}.")
    winner, scoreBoard = determine_winner(user_choice, computer_choice, scoreBoard)
    if winner == "None":
        print("*** It's a tie ***")
    else:
        print("*** "+winner+" wins ***")
    print(scoreBoard)
    print("Please remove your hand or press S to start again")
    return 1, scoreBoard, winner

def gameReset():
    isGameDone = False
    return isGameDone

def timeReset():
    saved_time = 0
    prev_saved_time = 0
    time_counter = 0
    current_time = time.time()
    previous_time = current_time
    return time_counter, prev_saved_time, saved_time, current_time, previous_time

def main():
    # Variable definitions
    cap = cv2.VideoCapture(3) # Start video capture from camera #1
    HandGes = HandGesRec() # HandGes fn.
    isIniSet = False
    isGameDone = False
    time_counter, prev_saved_time, saved_time, current_time, previous_time = timeReset()
    ref = {
    "Victory" : "scissors",
    "Closed_Fist" : "rock",
    "Open_Palm" : "paper"
    }
    prev_choice = "None" 
    scoreBoard = {
        "computerScore" : 0,
        "playerScore" : 0
    }
    winner = "None"

    while(1):
        ret, frame = cap.read()
        flipped_frame = cv2.flip(frame, 1)
        HandGes.detect(flipped_frame)
        fps = cap.get(cv2.CAP_PROP_FPS)
        user_choice = "None"

        if cv2.waitKey(int(200/fps))==ord('s'):
            isGameDone = gameReset()
            print("*** Game is now reset ***")
            
        if cv2.waitKey(int(200/fps))==ord('q'):
            break

        if HandGes.num_detected_hands>0: # If a hand is found, if not then loop
            user_choice = HandGes.get_gesture(0)

            if user_choice in list(ref.keys()): # if user choice is in list (of possible janken choices), prev = 
                prev_choice = user_choice 

                # CHECK IF INITIAL CHOICE IS SET
                if isIniSet == False:
                    ini_choice = user_choice
                    previous_time = time.time()
                    isIniSet = True
                    if isGameDone == False:
                        print("Your new choice is "+ref[user_choice])

                if user_choice == ini_choice and isGameDone == False:
                    # RESET TIME IF CHOICE HAS CHANGED
                    if (prev_choice != user_choice): # if previous choice doesnt match with curr choice
                        time_counter, prev_saved_time, saved_time, current_time, previous_time = timeReset()
                        isIniSet = False
                        continue
                    elif (prev_choice == user_choice): # ELSE TIMER RUNS NORMALY
                        current_time = time.time()
                        saved_time += m.floor(round(current_time - previous_time, 1))
                        if prev_saved_time != saved_time:
                            if time_counter == time_counter:
                                print(10-time_counter)
                            time_counter += 1
                        prev_saved_time = saved_time

                    # SHOW RESULT IF TIMER REACH 10s
                    if (time_counter >= 11): # Timer max to 10 seconds
                        computer_choice = get_computer_choice()
                        user_choice = ref[user_choice]
                        isGameDone, scoreBoard, winner = result(user_choice, computer_choice, scoreBoard)
                        time_counter, prev_saved_time, saved_time, current_time, previous_time = timeReset()
                else:
                    isIniSet = False
                    time_counter, prev_saved_time, saved_time, current_time, previous_time = timeReset()
        else:
            previous_time = time.time() # timer 0
            current_time = previous_time
            if isGameDone == True:
                isGameDone = gameReset()
                print("Game is now reset")

        annotated_frame = HandGes.visualize(flipped_frame)
        cv2.putText(annotated_frame, "{:d}:{:d}".format(scoreBoard["computerScore"], scoreBoard["playerScore"]), org=(300, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color=(255, 255, 255), thickness = 1, lineType=cv2.LINE_4)
        cv2.putText(annotated_frame, "Press Q to quit, Press S to restart", org=(40, 450), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color=(255, 255, 255), thickness = 1, lineType=cv2.LINE_4)
        if (isGameDone == True):
            if winner != "None":
                cv2.putText(annotated_frame, winner+ " win!", org=(100, 200), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 2, color=(0, 255, 0), thickness = 2, lineType=cv2.LINE_4)
            else:
                cv2.putText(annotated_frame, "It's a draw!", org=(100, 200), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 2, color=(0, 255, 0), thickness = 2, lineType=cv2.LINE_4)

        cv2.imshow('Janken game', annotated_frame)

    cv2.destroyAllWindows()
    cap.release() 

main()