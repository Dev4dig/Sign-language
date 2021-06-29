
import mediapipe as mp
import threading
import numpy as np
import autopy
import math
import matplotlib.pyplot as plt
import cv2
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
from threading import Thread
    
class Common:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
    
class Background:
    def __init__(self, c):
        self.common = c
    
    def run(self):
        i = 0
        flag_plus = True
        flag_minus = False
        while(True):
            
            # 1+(i*30), 1+(i*30), 500-(i*30), 500-(i*30)    ,x1,y1,x2,y2
            #time.sleep(0.5)
            if flag_plus:
                i =i+1
            if flag_minus:
                i = i-1
                
                
            if i == 200:
                flag_plus=False
                flag_minus=True
                #print("done.........100")
                
            if i == 1:
                flag_minus=False
                flag_plus=True
                #print("done.........1")
           
            self.common.x1 = 1+i
            self.common.y1 = 1+i
            self.common.x2 = 1000-i
            self.common.y2 = 1000-i
        # while loop ends
    
    
class Main:
    def __init__(self, background_thread_class, c):
        self.sceneH = 1000
        self.sceneW = 1000
        self.path = r'C:\\Users\Adnan Khan\Google Drive\FYP\Sign language\Experiments\3d.jpg'
        self.img1 = Image.open(self.path)
        self.img1 = self.img1.resize((self.sceneH,self.sceneW), Image.NEAREST)
        self.common = c
        
        bt = Thread(target=background_thread_class.run)
        bt.start()
        pass
    
    
    
    def zoom(self, x1,y1,x2,y2):
        print(str(x1))
        img = self.img1.crop((x1,y1,x2,y2))
        # img = img.resize((self.sceneH,self.sceneW), Image.NEAREST)
        img = np.array(img)
       
       
        resized = cv2.resize(img, (self.sceneH, self.sceneW), interpolation = cv2.INTER_AREA)
        #print(resized)
        cv2.imshow("Displaying", resized)

        
    
    def run(self):
        while True:
           print("running main")
           self.zoom(self.common.x1, self.common.y1, self.common.x2, self.common.y2)
           k = cv2.waitKey(1)
           #time.sleep(0.1)
           #break
        # while loop ends

common = Common()
background = Background(common)
mainClass = Main(background, common)
mainClass.run()



# path = r'C:\\Users\Adnan Khan\Google Drive\FYP\Sign language\Experiments\3d.jpg'
# # img = Image.open(path)
# # print(img)
# img = cv2.imread(path)
# cv2.imshow("Displaying", img)


# while True:
#     #print("running main")
#     #self.zoom(self.common.x1, self.common.y1, self.common.x2, self.common.y2)
#     #img = np.array(self.img1)
    
#     cv2.imshow("Displaying", img)
#     k = cv2.waitKey(1)
#     #time.sleep(0.5)
# # while loop ends