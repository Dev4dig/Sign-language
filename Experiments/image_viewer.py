
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

           
class ImageViewer(QtWidgets.QWidget):
    def __init__(self, i, gesture_thread):
        super().__init__()
        self.custom_width = 900
        self.custom_height = 600
        self.resize(self.custom_width,self.custom_height)
       
        #self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.image_pointer = 2
        
        #loading images from default directory
        self.default_img_dir = r"D:\test_images"
        self.img_list = os.listdir(self.default_img_dir)
        self.currentImg_path =  os.path.join(self.default_img_dir,self.img_list[self.image_pointer])
        
        #image dispaly label
        self.img_canvas = QtWidgets.QLabel(self)
        self.img_canvas.resize(self.custom_width,self.custom_height)
        #self.img_canvas.setStyleSheet("border: 2px solid rgb(255,0,0);")
        
        
        
        
          
        
            
        self.loadImage()
        
        
        
        self.interface = i
        self.gesture_thread = gesture_thread
        
        #registering events to gesture thread
        self.gesture_thread.signal_IVNext.connect(self.nextImg)
        self.gesture_thread.signal_IVPrev.connect(self.prevImg)
        self.gesture_thread.signal_IVZoom.connect(self.zoom)
        
        
        self.interface.Mode = com.Modes.IV_WINDOW
        self.setWindowTitle("Image Viewer ")
        
        #starting own thread
        Thread(target = self.run).start()
        self.thread = True
        
        #setting up focus handler
        self.setFocus()
        # app.focusChanged.connect(self.focusHandle)
        
        self.show()
    
    def focusHandle(self):
        print(self.isActiveWindow())
    
    def closeEvent(self,event):
        
        print("Window is being closed")
        reply =  msgBox.question(self, "Confirmation", "Are You Sure? ", msgBox.No | msgBox.Yes)
        print("----00")
        if reply == msgBox.Yes:
            print("----0")
            self.thread = False
            self.interface.Mode = com.Modes.MAIN_WINDOW
            print("----1")
           
            print("----2")
            event.accept()
            
        if reply == msgBox.No:
            pass
            event.ignore()
    #closeEvent

    #reset all zoom paramerters when image changs or first appears
    def calculate_zoom_params(self):
        self.zoomX1 = 0
        self.zoomY1 = 0
        self.zoomX2 = self.custom_width
        self.zoomY2 = self.custom_height
        
        self.zoomed_img = self.origonal_img
        self.max_zoom = int((self.custom_width/2) - (self.custom_width/20))
        self.current_zoom = 0 
        self.zoom_ratio_const = self.custom_width/self.custom_height
        print(str(self.zoom_ratio_const))
    def loadImage(self):
        
        self.currentImg_path = os.path.join(self.default_img_dir,self.img_list[self.image_pointer])
        self.origonal_img = Image.open(self.currentImg_path)
        
        self.calculate_zoom_params()
        
        # self.custom_width = self.img1.size[0]
        # self.custom_width = self.img1.size[1]
        self.origonal_img = self.origonal_img.resize((self.custom_width,self.custom_height), Image.NEAREST)
        self.displayImage(self.origonal_img)
    
    def displayImage(self,img):
        print("displayimg called")
        image = np.array(img)
        #img = np.array(self.img1)
        ima = QtGui.QImage(image.data, image.shape[1], image.shape[0], image.shape[1]*3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(ima)#.scaled(self.sceneH, self.sceneW)
        self.img_canvas.setPixmap(pix)
        # self.img_canvas.setPixmap(QtGui.QPixmap.fromImage(self.current_img))    
        
    def zoom(self,dist):
        
        
        if dist != 0:
            dist = int(dist/2)
            if dist < 0 :
                if self.current_zoom > 0:
                    if not self.current_zoom + dist < 0: 
                        self.current_zoom = self.current_zoom + dist
            elif dist > 0:
                 if self.current_zoom < self.max_zoom:
                        if self.current_zoom + dist < self.max_zoom: 
                            self.current_zoom = self.current_zoom + dist
                            
        print(str(self.current_zoom))
        print("============")
        self.zoomX1 = self.current_zoom
        self.zoomY1 = int(self.zoomX1/self.zoom_ratio_const)
        self.zoomX2 = self.custom_width - self.zoomX1
        self.zoomY2 = self.custom_height - self.zoomY1        
        
             
        self.zoomed_img = self.origonal_img.crop((self.zoomX1,self.zoomY1,self.zoomX2,self.zoomY2))#self.interface.zoomX1,self.interface.zoomY1,self.interface.zoomX2,self.interface.zoomY2
        self.zoomed_img = self.zoomed_img.resize((self.custom_width,self.custom_height), Image.NEAREST)
        self.displayImage(self.zoomed_img)
        pass
    
    
    def nextImg(self):
        if self.image_pointer < len(self.img_list)-1:
            print("True")
            self.image_pointer = self.image_pointer + 1
            
            self.loadImage()
        print("next image")
        
        pass
    
    def prevImg(self):
        if self.image_pointer > 0:
            print("True")
            self.image_pointer = self.image_pointer - 1
            
            self.loadImage()
        print("prev image")
        pass
    
    def run(self):
        # while self.thread:
        #     time.sleep(0.002)
        #     # if self.interface.Zoom:
        #     #     self.zoom()
        #print("IV thread Running")
        pass
            
           
            