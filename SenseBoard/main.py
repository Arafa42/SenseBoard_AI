from time import sleep

import cv2
from cvzone.HandTrackingModule import HandDetector

# INIT
finalText = ""
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
keys = [["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
        ["W", "X", "C", "V", "B", "N", ",", ";", ":", "="]]


# DRAW ALL BUTTONS
def drawAllButtons(img, buttonList):
    for buttons in buttonList:
        x, y = buttons.pos
        w, h = buttons.size
        cv2.rectangle(img, buttons.pos, (x + w, y + h), (42, 42, 42), cv2.FILLED)
        cv2.putText(img, buttons.text, (x + 25, y + 55), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)


# BUTTON CLASS
class Button():
    def __init__(self, pos, text, size=[75, 75]):
        self.pos = pos
        self.size = size
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text


buttonList = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([80 * j + 75, 100 * i + 75], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    drawAllButtons(img, buttonList)

    if len(hands) == 2:
        lmList1 = hands[0]["lmList"]  # List of 21 Landmark points
        lmList2 = hands[1]['lmList']
        if lmList1:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (120, 120, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 55), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
                    fingers1 = detector.fingersUp(hands[0])
                    if fingers1.count(1) > 1:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (220, 220, 220), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 25, y + 55), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
                        print(button)
                        finalText += str(button)
                        sleep(0.3)

        if lmList2:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                if x < lmList2[8][0] < x + w and y < lmList2[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (120, 220, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 55), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
                    fingers2 = detector.fingersUp(hands[1])
                    if fingers2.count(1) > 1:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (220, 220, 220), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 25, y + 55), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
                        print(button)
                        finalText += str(button)
                        sleep(0.3)


    cv2.putText(img, finalText, (169, 520),  cv2.FONT_HERSHEY_PLAIN, 7, (230, 230, 230), 5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
