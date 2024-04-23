import cv2
import mediapipe as mp
import pyautogui

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Edge()
driver.get('https://www.youtube.com/watch?v=7bjpguXESI8')
video = driver.find_element(By.ID,'movie_player')

wCam , hCam = 648 , 488
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

x1 = y1 = x2 = y2 = 0
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    success , img = cap.read()
    img = cv2.flip(img , 1)
    frame_height , frame_width , _ = img.shape
    rgb_image = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(img , hand)
            landmarks = hand.landmark
            for id , landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img = img , center=(x,y) , radius = 8 , color = (0,255,255) , thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv2.circle(img = img , center=(x,y) , radius = 8 , color = (0,0,255) , thickness=3)
                    x2 = x
                    y2 = y
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),5)
        dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4
        if dist > 20:
            video.send_keys(Keys.ARROW_UP)
        else:
            video.send_keys(Keys.ARROW_DOWN)
    
    
    
    cv2.imshow("Volume Control" , img)
    key = cv2.waitKey(10)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
