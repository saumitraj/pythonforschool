import cv2
from chardet import detect
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=1, detectionCon=0.8)
video = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

cv2.startWindowThread()

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

while True:
    _, img = cap.read()
    #img = cv2.flip(img, 1)
    hand, img = detector.findHands(img)
    text = 'Count : 0'
    if hand:
        if hand[0]:
            fingerup = detector.fingersUp(hand[0])
            print(fingerup)
            text = 'Count : ' + str(fingerup.count(1))
            if fingerup == [1,0,0,0,0]:
                text = 'Thumbs up'

            cv2.putText(img,
                        text,
                        (50, 50),
                        font, 1,
                        (255, 0, 0),
                        4,
                        cv2.LINE_4)
    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()