import vs_com_interface as com
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
from threading import Thread
import cv2
from PyQt5.QtCore import Qt
import numpy as np

class PaintApp(QtWidgets.QWidget):
    def __init__(self, i, gesture_thread):
        super().__init__()
        self.interface = i
        self.gesture_thread = gesture_thread
        self.thread = True
        
        self.height_ = self.interface.CANVAS_H
        self.width_ = self.interface.CANVAS_W
        
        self.brush_thickness = 5
        self.drawing_color = (255,255,0)
        self.header_path = r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\Experiments/h.png'
        self.header_img = cv2.imread(self.header_path)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        
        #setting app mode to paint 
        self.interface.Mode = com.Modes.PAINT_WINDOW
        self.setWindowTitle("Paint App")
        self.resize(self.width_, self.height_)
        
        
        self.canvas = QtWidgets.QLabel(self)
        self.canvas.resize(self.width_, self.height_)
        self.canvas.setStyleSheet("border:2px solid rgb(255, 0,0);")
        
        self.drawing_canvas = np.zeros((self.height_, self.width_, 3), np.uint8)
       
        
        #registering Events listeners
        self.gesture_thread.signal_PaintDrawMode.connect(self.onDraw)
        self.gesture_thread.signal_PaintSelectMode.connect(self.onSelect)
        
        self.show()
        
    def onDraw(self, x, y, image):
        #cv2.imshow("camera",image)
        image[0:60, 0:850] = self.header_img
        imgGray = cv2.cvtColor(self.drawing_canvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        image = cv2.bitwise_and(image, imgInv)
        image = cv2.bitwise_or(image, self.drawing_canvas)
    
        cv2.line(self.drawing_canvas, (10,10), (self.width_-10, self.height_-10), self.drawing_color, self.brush_thickness)
        image = self.drawing_canvas
        ima = QtGui.QImage(image.data, image.shape[1], image.shape[0], image.shape[1]*3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(ima)#.scaled(self.width_, self.height_)
        self.canvas.setPixmap(pix)
        #print(object)
        pass
    
    def onSelect(self, x, y):
        print("Select mode")
        pass
        
    def closeEvent(self, event):
        print("Window is being closed")
        self.thread = False
        self.interface.Mode = com.Modes.MAIN_WINDOW
        event.accept()
    
    def run(self):
        
        while self.thread:
            
            pass