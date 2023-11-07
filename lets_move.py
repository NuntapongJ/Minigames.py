# mypose_simple.py
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
from MediapipePoseLandmark import MediapipePoseLandmark as PoseLmk
import pandas as pd

df = pd.read_csv("./Beatmap/sign_b.csv")
#print(df.filter(items=["LX","LY","RX","RY"]).values)

LeftHand = (df.filter(items=["LX","LY"]).to_numpy()).tolist()
RightHand = (df.filter(items=["RX","RY"]).to_numpy()).tolist()
bothHand = []

for i in range(len(LeftHand)):
    bothHand.append([LeftHand[i],RightHand[i]])

cap = cv2.VideoCapture(3)
Pose = PoseLmk()
note_id = 0
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    Pose.detect(frame)
    masks = Pose.get_all_segmentation_masks()
    masked_frame = Pose.visualize_mask(frame, masks)
    annotated_frame = Pose.visualize_with_mp(masked_frame)
    # 15R 16L

    try:
        # print(Pose.get_normalized_landmark(0,16),Pose.get_normalized_landmark(0,15))
        # if (Pose.get_normalized_landmark(0,15)[1] < 0.5):
        #     print("UpperR")
        # if (Pose.get_normalized_landmark(0,16)[1] < 0.5):
        #     print("UpperL")

        # # Calibrator
        # obj_center_pointX = (frame.shape[1] * Pose.get_normalized_landmark(0,11)[0] + frame.shape[1] * Pose.get_normalized_landmark(0,12)[0])//2
        # obj_center_pointY = (frame.shape[0] * Pose.get_normalized_landmark(0,11)[1] + frame.shape[0] * Pose.get_normalized_landmark(0,12)[1])//2
        # obj_radius = 400
        
        # cv2.rectangle(annotated_frame,(int(obj_center_pointX - obj_radius),int(obj_center_pointY - obj_radius)),(int(obj_center_pointX + obj_radius),int(obj_center_pointY + obj_radius)),(255,0,0),2)
        frame_centerX = frame.shape[1] // 2
        frame_centerY = frame.shape[0] // 2

        #Actual Hands
        leftX = int(Pose.get_normalized_landmark(0,16)[0] * frame.shape[1])
        leftY = int(Pose.get_normalized_landmark(0,16)[1] * frame.shape[0])
        rightX = int(Pose.get_normalized_landmark(0,15)[0] * frame.shape[1])
        rightY = int(Pose.get_normalized_landmark(0,15)[1] * frame.shape[0])

        # print(leftX,leftY," - ",rightX,rightY)

        # Notes
        left_note = bothHand[note_id % len(bothHand)][0]
        right_note = bothHand[note_id % len(bothHand)][1]

        note_radius = 30


        # Left Static
        cv2.rectangle(annotated_frame,(left_note[0] - note_radius + frame_centerX,left_note[1] * (-1) - note_radius + frame_centerY),(left_note[0] + note_radius + frame_centerX,left_note[1] * (-1) + note_radius + frame_centerY),(0,255,0),2)
        
        # Right Static
        cv2.rectangle(annotated_frame,(right_note[0] - note_radius + frame_centerX,right_note[1] * (-1) - note_radius + frame_centerY),(right_note[0] + note_radius + frame_centerX,right_note[1] * (-1) + note_radius + frame_centerY),(0,0,255),2)
        
        # print("(" + str(leftX) + "," + str(leftY) + ")","(" + str(rightX) + "," + str(rightY) + ")")

        isL = isR = False
        #Left Detect
        if (leftX >= left_note[0] - note_radius + frame_centerX and leftX <= left_note[0] + note_radius + frame_centerX):
            if (leftY >= left_note[1] * (-1) - note_radius + frame_centerY and leftY <= left_note[1] * (-1) + note_radius + frame_centerY):
                isL = True

        #Right Detect
        if (rightX >= right_note[0] - note_radius + frame_centerX and rightX <= right_note[0] + note_radius + frame_centerX):
            if (rightY >= right_note[1] * (-1) - note_radius + frame_centerY and rightY <= right_note[1] * (-1) + note_radius + frame_centerY):
                isR = True
        
        if (isL and isR):
            note_id += 1
            print(note_id)

        # print(right_note[0] - note_radius + frame_centerX)
        # print(right_note[0] + note_radius + frame_centerX)
        # print(right_note[1] * (-1) - note_radius + frame_centerY)
        # print(right_note[1] * (-1) + note_radius + frame_centerY)
        # Right Static
        # cv2.rectangle(annotated_frame,(int(right_note[0] - note_radius + frame_centerX),int(right_note[0] + note_radius + frame_centerX)),(int(right_note[1] * (-1) - note_radius + frame_centerY),int(right_note[1] * (-1) + note_radius + frame_centerY)),(0,0,255),2)
        
        # #left
        # cv2.rectangle(annotated_frame, ((int(left_note[0] - note_radius)),(int(obj_center_pointY + left_note[1] * (-1) - note_radius))),(int(obj_center_pointX + left_note[0] + note_radius),(int(obj_center_pointY + left_note[1] * (-1) + note_radius))),(0,0,255),2)
        
        # #right
        # cv2.rectangle(annotated_frame, (int(right_note[0] - note_radius),(int(obj_center_pointY + right_note[1] * (-1) - note_radius))),(int(obj_center_pointX + right_note[0] + note_radius),(int(obj_center_pointY + right_note[1] * (-1) + note_radius))),(0,0,0),2)

        # Right Detect on Edge
        

        cv2.imshow('frame', annotated_frame)
        key = cv2.waitKey(1)&0xFF
        if key == ord('q'):
            break
        if key == ord('n'):
            note_id += 1
            print(note_id)
        if key == ord('p'):
            note_id -= 1
            print(note_id)
    except Exception:
        pass
cv2.destroyAllWindows()
Pose.release()
cap.release()