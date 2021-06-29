from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import matplotlib.pyplot as plt
import os
import time
from threading import Thread
from queue import Queue
import cv2
import numpy as np

class UI_Window(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle('Main')
        self.resize(800,650)
        self.background_thread = Background_Thread()
        self.background_thread.start()
        self.background_thread.signal.connect(self.rescaleImage)
        
        self.path = r'C:\Users\Adnan Khan\Google Drive\FYP\d.JPG'
        self.img = cv2.imread(self.path)  #h,w,channel
        self.win_frame_w = 100
        self.win_frame_h = 100
        self.window_frame = np.zeros((self.win_frame_h, self.win_frame_w, 3), np.uint8) # h,w,channels
        
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(10,10, self.win_frame_w, self.win_frame_h))
        self.label_3.setObjectName("label_3")
        self.retranslate()
        # self.rescaleImage((2000,2000))
                 
        
        
        
    def get_signal(self, val, val2):
        b=str(val)+str(val2)
        self.label_3.setText( b)
        print( b)
        
    def rescaleImage(self,w,h):
        st = str(w)+str(h)
        
        print(st)
        dim = (w,h)
        resized = cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)
        start_x = int((resized.shape[1]-self.win_frame_w)/2)
        start_y = int((resized.shape[0]-self.win_frame_h)/2)
        for height in range(self.win_frame_h):
            for width in range(self.win_frame_w):
                for channel in range(3):
                    self.window_frame[height][width][channel]= resized[height+start_y-1][width+start_x-1][channel] 

        ima = QtGui.QImage(self.window_frame.data, self.window_frame.shape[1], self.window_frame.shape[0], self.window_frame.shape[1]*3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(ima).scaled(self.win_frame_w, self.win_frame_h)
        self.label_3.setPixmap(pix)
       
        print("log two")        
    def retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_3.setText(_translate("MainWindow", "image Label"))
        
# ==========================================

class Background_Thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int, int)
    def __init__(self, parent=None):
        super(Background_Thread,self).__init__(parent)
        
    def run(self):
        i = 0
        while(True):
            self.signal.emit(600+(i*30),600+(i*30))
            i = i+1
            time.sleep(0.1)
        


   

app = QtWidgets.QApplication(sys.argv)   
w = UI_Window()
w.show()
    
sys.exit(app.exec_())
