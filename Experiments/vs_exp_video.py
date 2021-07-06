


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
import sys



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gesture App")
        self.resize(800,800)
        self.sceneW = 500
        self.sceneH = 500
        self.addGraphics()
        self.cap = cv2.VideoCapture(0)
        self.background_thread = Background_Thread()
        self.background_thread.start()
        self.background_thread.signal.connect(self.run)

    def addGraphics(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.blakBrush = QtGui.QBrush(QtCore.Qt.black)
        self.bluePen = QtGui.QPen(QtCore.Qt.blue)
        self.graphicView = QtWidgets.QGraphicsView(self.scene, self)
        self.graphicView.setGeometry(0,0,self.sceneW, self.sceneH)
         
        
    def run(self,s):
        
        
        success, img = self.cap.read()
        
        if success:
            # img = cv2.flip(img, 1)
            # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # ih, iw, ic = img.shape
            
            resized = cv2.resize(img, (self.sceneH, self.sceneW), interpolation = cv2.INTER_AREA)
    
            # ima = QtGui.QImage(resized.data, resized.shape[1], resized.shape[0], resized.shape[1]*3, QtGui.QImage.Format_RGB888)
            # pix = QtGui.QPixmap(ima).scaled(self.sceneH, self.sceneW)
            # self.scene.addPixmap(pix)
            cv2.imshow("Experiments",resized)
        #end if success
    #end run
    
    
class Background_Thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(Background_Thread,self).__init__(parent)
        
    def run(self):
        while(True):
            time.sleep(0.05)
            self.signal.emit(1)
    
    
app = QtWidgets.QApplication(sys.argv)   
w = MainWindow()
w.show()
    
sys.exit(app.exec_())