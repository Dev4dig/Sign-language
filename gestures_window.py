
import vs_com_interface as com
import numpy as np 
import cv2
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
from threading import Thread
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox as msgBox
import os

           
class GestureViewer(QtWidgets.QWidget):
    def __init__(self, i, gesture_thread):
        super().__init__()
        self.custom_width = 600
        self.custom_height = 600
        self.resize(self.custom_width,self.custom_height)
        self.interface = i
        self.gesture_thread = gesture_thread
        self.path = r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\signs'
        self.interface.Mode = com.Modes.GV_WINDOW
        self.setWindowTitle("Gesture Viewer ")
        
    
        self.gesture_sign = QtWidgets.QLabel(self)
        self.gesture_sign.resize(600,600)
        self.gesture_sign.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(os.path.join(self.path,'one.jpg')).scaled(450, 400)))
        self.sign_images = [
            'hand_close.jpg',
            'one.jpg',
            'two.jpg',
            'three.jpg',
            'four.jpg',
            'five.jpg', 
            'close_gesture.jpg',
            'left_close.jpg',
            'right_close.jpg',
            'right.png',
            'left.png', 
            'left_click.jpg', 
            'right_click.jpg', 
            'zoom.png'
            ]
            
            
           
            
            
            
            
        self.sign_imgs_paths = os.listdir(self.path)
        print(self.sign_images)
        
        self.sign_imgs = []
        index = 0 
        for i in self.sign_imgs_paths:
            self.sign_imgs.append(QtGui.QPixmap.fromImage(QtGui.QImage(os.path.join(self.path,self.sign_images[index])).scaled(600, 400)))
            index = index+1
        
        print(self.sign_imgs)
        # register events
        self.gesture_thread.signal_GVClose.connect(self.closeCustom)
        self.gesture_thread.signal_GV_ONE.connect(self.one)
        self.gesture_thread.signal_GV_TWO.connect(self.two)
        self.gesture_thread.signal_GV_THREE.connect(self.three)
        self.gesture_thread.signal_GV_FOUR.connect(self.four)
        self.gesture_thread.signal_GV_FIVE.connect(self.five)
        self.gesture_thread.signal_GV_HAND_CLOSE.connect(self.hand_close)
        self.gesture_thread.signal_GV_POINT_RIGHT.connect(self.point_right)
        self.gesture_thread.signal_GV_POINT_LEFT.connect(self.point_left)
        
        self.gesture_thread.signal_GV_RIGHT_CLICK.connect(self.right_click)
        self.gesture_thread.signal_GV_LEFT_CLICK.connect(self.left_click)
        self.gesture_thread.signal_GV_LEFT_CLOSE.connect(self.left_close)
        self.gesture_thread.signal_GV_RIGHT_CLOSE.connect(self.right_close)
        
        self.gesture_thread.signal_GV_ZOOM.connect(self.zoom)
        
        self.show()
        
    
    def one(self):
        self.gesture_sign.setPixmap(self.sign_imgs[1])
        print("one --")
    
    def two(self):
        self.gesture_sign.setPixmap(self.sign_imgs[2])
        print("two --")
    
    def three(self):
        self.gesture_sign.setPixmap(self.sign_imgs[3])
        print("three --")
    
    def four(self):
        self.gesture_sign.setPixmap(self.sign_imgs[4])
        print("four --")
    
    def five(self):
        self.gesture_sign.setPixmap(self.sign_imgs[5])
        print("five --")
    
    def point_right(self):
        self.gesture_sign.setPixmap(self.sign_imgs[9])
        print("point_right --")
    
    def point_left(self):
        self.gesture_sign.setPixmap(self.sign_imgs[10])
        print("point_left --")
    
    def zoom(self):
        self.gesture_sign.setPixmap(self.sign_imgs[13])
        print("zoom --")
    
    def right_click(self):
        self.gesture_sign.setPixmap(self.sign_imgs[12])
        print("right_click --")
    
    def left_click(self):
        self.gesture_sign.setPixmap(self.sign_imgs[11])
        print("left_click --")
    
    def hand_close(self):
        self.gesture_sign.setPixmap(self.sign_imgs[0])
        print("hand_close --")
    
    def left_close():
        self.gesture_sign.setPixmap(self.sign_imgs[7])
        print("left CLose")
        
    def right_close():
        self.gesture_sign.setPixmap(self.sign_imgs[8])
        print("right CLose")
  
    def closeCustom(self):
        print("Window is being closed")
        self.thread = False
        self.interface.Mode = com.Modes.MAIN_WINDOW
        self.close()