import time
from PyQt5 import QtCore
import vs_com_interface as com
import cv2

class Gestures(QtCore.QThread):
    signal_mainPaint = QtCore.pyqtSignal()
    signal_mainIV = QtCore.pyqtSignal()
    signal_IVNext = QtCore.pyqtSignal()
    signal_IVPrev = QtCore.pyqtSignal()
    signal_IVZoom = QtCore.pyqtSignal(int,int,int,int)
     
    #paint signals
    signal_PaintDrawMode = QtCore.pyqtSignal(int, int, object)
    signal_PaintSelectMode = QtCore.pyqtSignal(int, int)
    
    #signal_IVZoom = QtCore.pyqtSignal()
    def __init__(self, c, parent=None):
        super(Gestures,self).__init__(parent)
        self.i= 0
        self.interface = c
        pass
     
    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            time.sleep(0.01)
            
            success, img = cap.read()
            img = cv2.resize(img, (self.interface.CANVAS_W, self.interface.CANVAS_H))
            
            if success:
                if(self.interface.Mode == com.Modes.PAINT_WINDOW):
                    self.signal_PaintDrawMode.emit(5,6,img)
                
            print("Gesture Emulator Running...")
            # print(self.interface.Mode)
            # if(self.interface.Mode == com.Modes.PAINT_WINDOW):
            #     self.signal_PaintDrawMode.emit(5,6)
            #     self.signal_PaintSelectMode.emit(5,6)
            #     pass
    
    
    
    #zoom emulator
    # def run(self):
    #     i = 1
    #     flag_plus = True
    #     flag_minus = False
    #     while True:
    #         time.sleep(0.001)
    #         # 1+(i*30), 1+(i*30), 500-(i*30), 500-(i*30)    ,x1,y1,x2,y2
            
            
    #         #i = i+1
    #         if flag_plus:
    #             i =i+1
    #         if flag_minus:
    #             i = i-1
                
                
    #         if i > 100:
    #             flag_plus=False
    #             flag_minus=True
    #             print("top reached")
                
                
    #         if i == 1:
    #             flag_minus=False
    #             flag_plus=True
    #             print("floor reached") 
        
    #         if self.interface.Mode == com.Modes.IV_WINDOW:
    #             print("calling zoom")
    #             self.signal_IVZoom.emit(2+i,1+i,900-(i*2),600-i)
                
    #         print(i)
            
           
            
            