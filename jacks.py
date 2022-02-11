import cv2
import cvzone.PoseModule as pm
import numpy as np

cap = cv2.VideoCapture(0)
detector = pm.PoseDetector()

count = 0
direction = 0

angle1_list = []
angle2_list = []
while True:
    _, img = cap.read()
    img = cv2.resize(img, (700, 540))
    img = cv2.flip(img, 1)
    image = detector.findPose(img, draw=False)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        angle2 = detector.findAngle(img, 24, 12, 14, draw=True)
        angle1 = detector.findAngle(img, 23, 11, 13, draw=True)
        angle1_list.append(angle1)
        angle2_list.append(angle2)
        per1 = 100 - np.interp(angle1, (200, 330), (0, 100))
        per2 = np.interp(angle2, (40, 160), (0, 100))
        print(per1)
        if len(angle1_list) > 2 and len(angle2_list) > 2:
            # print(angle_list[-2], angle_list[-1])
            if angle1_list[-2] - angle1_list[-1] > 300 and angle2_list[-2] - angle2_list[-1] < -300:
                count -= 0.5
        if per1 and per2 == 100:
            if direction == 0:
                count += 0.5
                direction = 1

        if per1 and per2 == 0:
            if direction == 1:
                count += 0.5
                direction = 0

        cv2.rectangle(img, (0, 0), (200, 200), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(count)}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 10)
    cv2.imshow("Image", image)
    if cv2.waitKey(1) == ord('c'):
        break
cap.release()
cv2.destroyAllWindows()
