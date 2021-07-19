#import vs_detection_module as gestues
import vs_gesture_emulator as GE
import vs_com_interface as com
from image_viewer import ImageViewer
from paint import PaintApp
from vs_detection_module import *
import os
from threading import Thread
import numpy as npcl

import math
import matplotlib.pyplot as plt
import cv2
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
from threading import Thread
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox as msgBox
from PIL import Image
 
#B20CBF
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, i, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gesture App")
        self.resize(600,400)
        self.interface = i 
        #setting App mode which will b sync signal that app is currently in main screen
        self.interface.Mode = com.Modes.MAIN_WINDOW
        
        #starting Background Thread
        self.gesture_thread = Detection_Module(self.interface)
        
        #registering events listeners
        self.gesture_thread.signal_mainPaint.connect(self.launch_paint)
        self.gesture_thread.signal_mainIV.connect(self.launch_imgViewer) 

        #starting gesture thread
        self.gesture_thread.start()
        
        self.path = r'C:\Users\Adnan Khan\Downloads\back.jpg'
        self.background_container = QtWidgets.QLabel(self)
        self.background_container.resize(600,400)
        self.background_container.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(self.path).scaled(600, 400)))
        #self.background_container.setStyleSheet("border-radius: 15px;")    
        #self.setWindowFlags(Qt.FramelessWindowHint)
        
        #self.setStyleSheet(" background-color:rgba(255,0,0,200); ")
        
        self.Title = QtWidgets.QLabel(self)
        self.Title.move(137, 15)
        self.Title.resize(330, 20)
        self.Title.setText("Gesture Recognition System developed by: ADNAN KHAN")
        self.Title.setStyleSheet("border-radius:3px; background-color:rgba(0, 0, 0, 125); color: rgba(255, 255, 255, 150); font-size:13px; border: 1px solid rgba(255,255,255,100);")
        
        
        self.openPaintBtn_1 = QtWidgets.QPushButton(self)
        self.openPaintBtn_1.setText("Paint")
        self.openPaintBtn_1.move(145,65)
        self.openPaintBtn_1.resize(150,150)
        #self.openPaintBtn_1.setStyleSheet("background-color: #FF0000;")
        self.openPaintBtn_1.setStyleSheet("border: 2px solid  rgba(255,255,255, 100); border-radius: 5px; background-color: rgba(0, 0, 0, 125); color: rgb(255, 255, 255);")
        self.openPaintBtn_1.clicked.connect(self.launch_paint)
        
        self.openImageViewerBtn_2 = QtWidgets.QPushButton(self)
        self.openImageViewerBtn_2.setText("Image Viewer")
        self.openImageViewerBtn_2.move(305,65)
        self.openImageViewerBtn_2.resize(150,150)
        self.openImageViewerBtn_2.setStyleSheet("border: 2px solid  rgba(255,255,255, 100); border-radius: 5px; background-color: rgba(0, 0, 0, 125); color: rgb(255, 255, 255);")
        self.openImageViewerBtn_2.clicked.connect(self.launch_imgViewer)
        
        #self.setStyleSheet("background-color: #FF0000;");
        
        self.openGesturesViewBtn_3 = QtWidgets.QPushButton(self)
        self.openGesturesViewBtn_3.setText("Gesture Viewer")
        self.openGesturesViewBtn_3.move(225, 225)
        self.openGesturesViewBtn_3.resize(150,150)
        self.openGesturesViewBtn_3.setStyleSheet("border: 2px solid  rgba(255,255,255, 100); border-radius: 5px; background-color: rgba(0, 0, 0, 125); color: rgb(255, 255, 255);")
        self.openGesturesViewBtn_3.clicked.connect(self.launch_GesturesView)
        
        
        self.crossLabel = QtWidgets.QLabel(self)
        self.crossLabel.move(570,5)
        self.crossLabel.resize(27,27)
        self.crossLabel.setText("x")
        self.crossLabel.setStyleSheet("border:1px solid rgb(255,255,255);padding-top:0px; border-radius: 3px; padding-bottom:4px; font-size: 26px;color: rgba(255,255,255,200); background-color:rgba(255,0,0, 50);")
        

    def closeEvent(self, event):
        print("Window is being closed")
        
        
    def launch_paint(self):
        self.paintWindow = PaintApp(self.interface, self.gesture_thread)
        print("launch paint")
       
        
    def launch_imgViewer(self):
        self.IV = ImageViewer(self.interface, self.gesture_thread)
        print("launch iv")
        
    
    def launch_GesturesView(self):
        pass
    
    
    def enableWindow(self):
        self.isEnabled(True)
        
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#==========================================================




#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#==========================================================




# dm = gestues.Detection_Module(2)
# gesture_thread = Thread(target=dm.run)
# gesture_thread.start()



app = QtWidgets.QApplication(sys.argv)
c = com.Com_interface()
mainWindow = MainWindow(c)


mainWindow.show()     
sys.exit(app.exec_())
