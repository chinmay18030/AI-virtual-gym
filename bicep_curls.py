"""
This program is for bicep curls, stand in a way so that your left arm faces the camera (https://i.ytimg.com/vi/in7PaeYlhrM/maxresdefault.jpg stand in a way like this, 
so that the left arm faces the camera like this)

"""
import cv2
import cvzone.PoseModule as pm
import numpy as np

cap = cv2.VideoCapture(0)
detector = pm.PoseDetector()

count = 0
direction = 0

angle_list = []
while True:
    _, img = cap.read()
    img = cv2.resize(img, (700, 540))
    img = cv2.flip(img, 1)
    image = detector.findPose(img, draw=False)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        angle = detector.findAngle(img, 11, 13, 15, draw=True)
        angle_list.append(int(angle))

        if len(angle_list) > 2:
            # print(angle_list[-2], angle_list[-1])
            if angle_list[-2] - angle_list[-1] > 300:
                count -= 1

        ngle = np.interp(angle, (210, 310), (0, 100))

        if ngle == 100:
            if direction == 0:
                count += 0.5
                direction = 1
        if ngle == 0:
            if direction == 1:
                count += 0.5
                direction = 0
        print(count)
        cv2.rectangle(img, (0, 0), (200, 200), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(count)}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 10)
    cv2.imshow("Image", image)
    if cv2.waitKey(1) == ord('c'):
        break
cap.release()
cv2.destroyAllWindows()
