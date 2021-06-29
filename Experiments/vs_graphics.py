from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
from PIL import Image
from PIL.ImageQt import ImageQt
import time
from threading import Thread
import numpy as np

class UI_Window(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle('Main')
        self.resize(800,650)
        
        #thread setup
        self.background_thread = Background_Thread()
        self.background_thread.start()
        self.background_thread.signal.connect(self.zoom)
        
        
        self.sceneW = 500
        self.sceneH = 500
        self.addGraphics()
        self.zoom(10,10, 500,500)
        
    def addGraphics(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.blakBrush = QtGui.QBrush(QtCore.Qt.black)
        self.bluePen = QtGui.QPen(QtCore.Qt.blue)
        self.graphicView = QtWidgets.QGraphicsView(self.scene, self)
        self.graphicView.setGeometry(0,0,self.sceneW, self.sceneH)
        
        self.path = r'C:\Users\Adnan Khan\Google Drive\FYP\d.JPG'
        self.img1 = Image.open(self.path)
        self.img1 = self.img1.resize((self.sceneH,self.sceneW), Image.NEAREST)
    
    def zoom(self, x1,y1,x2,y2):
        # print(str(x2))
        img = self.img1.crop((x1,y1,x2,y2))
        # img = img.resize((self.sceneH,self.sceneW), Image.NEAREST)
        img = np.array(img)
        resized = cv2.resize(img, (self.sceneH, self.sceneW), interpolation = cv2.INTER_AREA)
        
        ima = QtGui.QImage(resized.data, resized.shape[1], resized.shape[0], resized.shape[1]*3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(ima).scaled(self.sceneH, self.sceneW)
        self.scene.addPixmap(pix)
    
    def flipRight(self):
        pass

    def flipLeft(self):
        pass
    
    def flipUp(self):
        pass
    
    def flipDown(self):
        pass


class Background_Thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int, int,int,int)
    def __init__(self, parent=None):
        super(Background_Thread,self).__init__(parent)
        
    def run(self):
        i = 0
        flag_plus = True
        flag_minus = False
        while(True):
            
            # 1+(i*30), 1+(i*30), 500-(i*30), 500-(i*30)    ,x1,y1,x2,y2
            time.sleep(0.01)
            
            
            if flag_plus:
                i =i+1
            if flag_minus:
                i = i-1
                
                
            if i == 100:
                flag_plus=False
                flag_minus=True
                print("done.........100")
                
            if i == 1:
                flag_minus=False
                flag_plus=True
                print("done.........1")
            print(i)
            self.signal.emit(1+(i*2), 1+(i*2), 500-(i*2), 500-(i*2))
            
            
            
app = QtWidgets.QApplication(sys.argv)   
w = UI_Window()
w.show()
    
sys.exit(app.exec_())