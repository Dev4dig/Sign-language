
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
        
        self.gesture_thread.signal_IVZoomDrag.connect(self.drag_img)
        
        
        self.interface.Mode = com.Modes.IV_WINDOW
        self.setWindowTitle("Image Viewer ")
        
        #starting own thread
        Thread(target = self.run).start()
        self.thread = True
        
        #setting up focus handler
        self.setFocus()
        # app.focusChanged.connect(self.focusHandle)
        
        self.show()
    #=======================================================================================================
    def focusHandle(self):
        print(self.isActiveWindow())
    #=======================================================================================================
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
    #=======================================================================================================
    #reset all zoom paramerters when image changs or first appears
    def calculate_zoom_params(self):
        
        self.zoomX1 = 0
        self.zoomY1 = 0
        self.zoomX2 = self.custom_width
        self.zoomY2 = self.custom_height
         
        self.zoomed_img = self.origonal_img 
        self.maxZoom_verticle = int(self.custom_height - (self.custom_height/10))
        self.maxZoom_horizontal = int(self.custom_width - (self.custom_width/10))
        
               
        self.zoom_ratio_const = self.custom_width/self.custom_height
        
        self.calculate_margins()
                       
    #=======================================================================================================    
    def calculate_margins(self):
        self.a = self.zoomX1 
        self.b = self.custom_width - self.zoomX2
        self.p = self.zoomY1
        self.q = self.custom_height - self.zoomY2
        
        cx = int((self.zoomX2 - self.zoomX1)/2)
        cy = int((self.zoomY2 - self.zoomY1)/2)
        self.calculate_center_params(x = cx, y =cy) #first time by default zoom at center
    #=======================================================================================================    
    def calculate_center_params(self, x ,y ):
        self.zoom_centerX = x
        self.zoom_centerY = y
        
        self.u = self.zoom_centerY #up from center
        self.d = int(self.custom_height-self.zoom_centerY)#down from center
        self.l = self.zoom_centerX #left from center
        self.r = int(self.custom_width-self.zoom_centerX) #down from centre
        
        
    
    #=======================================================================================================    
    def loadImage(self):
        
        self.currentImg_path = os.path.join(self.default_img_dir,self.img_list[self.image_pointer])
        self.origonal_img = Image.open(self.currentImg_path)
        
        self.calculate_zoom_params()
        
        # self.custom_width = self.img1.size[0]
        # self.custom_width = self.img1.size[1]
        self.origonal_img = self.origonal_img.resize((self.custom_width,self.custom_height), Image.NEAREST)
        self.displayImage(self.origonal_img)
    
    
    
    #=======================================================================================================
    def displayImage(self,img):
        #print("displayimg called")
        image = np.array(img)
        #img = np.array(self.img1)
        ima = QtGui.QImage(image.data, image.shape[1], image.shape[0], image.shape[1]*3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(ima)#.scaled(self.sceneH, self.sceneW)
        self.img_canvas.setPixmap(pix)
        # self.img_canvas.setPixmap(QtGui.QPixmap.fromImage(self.current_img))   
        
         
    #=======================================================================================================
    #=======================================================================================================
    #=======================================================================================================    
    def zoom(self,dist):
        
        
        if dist != 0:
            
            if dist > 0:
                dist = dist * 2
                
                if (self.a + self.b + dist) < self.maxZoom_horizontal   and (self.p + self.q + int((dist/self.zoom_ratio_const))) < self.maxZoom_verticle :
                    self.a = self.a + int(((dist / self.custom_width) * self.l))
                    self.b = self.b + int(((dist / self.custom_width) * self.r))
                    self.p = self.p + int((((dist / self.custom_height) * self.u) / self.zoom_ratio_const))
                    self.q = self.q + int((((dist / self.custom_height) * self.d) / self.zoom_ratio_const))
                    
            elif dist < 0:
                dist = dist * 3
                temp_a = self.a + int(((dist / self.custom_width) * self.l))
                temp_b = self.b + int(((dist / self.custom_width) * self.r))
                temp_p = self.p + int((((dist / self.custom_height) * self.u) / self.zoom_ratio_const))
                temp_q = self.q + int((((dist / self.custom_height) * self.d) / self.zoom_ratio_const))
                
                if temp_a > 0:
                    self.a = temp_a
                if temp_b > 0:
                    self.b = temp_b
                if temp_p > 0:
                    self.p = temp_p
                if temp_q > 0:
                    self.q = temp_q
                    
                
                    
       
        self.zoomX1 = self.a
        self.zoomY1 = self.p   
        self.zoomX2 = self.custom_width - self.b
        self.zoomY2 = self.custom_height - self.q 
      
             
        self.zoomed_img = self.origonal_img.crop((self.zoomX1,self.zoomY1,self.zoomX2,self.zoomY2))#self.interface.zoomX1,self.interface.zoomY1,self.interface.zoomX2,self.interface.zoomY2
        self.zoomed_img = self.zoomed_img.resize((self.custom_width,self.custom_height), Image.NEAREST)
        self.displayImage(self.zoomed_img)
        
        
        cx = int((self.zoomX2 - self.zoomX1)/2)
        cy = int((self.zoomY2 - self.zoomY1)/2)
        self.calculate_center_params(x = cx, y =cy)
        pass
    #=======================================================================================================
    #=======================================================================================================
    #=======================================================================================================
    def drag_img(self, x,y):
        #this will adjust the croping coordinates of image and readust the margins accordingly
        #then will show the croped image 
        
        x = x*2
        y = y*2
        tempX1 = int(self.zoomX1 - x)
        tempX2 = int(self.zoomX2 - x)
        
        tempY1 = int(self.zoomY1 - y)
        tempY2 = int(self.zoomY2 - y)
        
        condX1 = (not (tempX1 < 0   or   tempX1 > self.maxZoom_horizontal))
        condX2 = (not (tempX2 < (self.custom_width - self.maxZoom_horizontal)   or   tempX2 > self.custom_width))
        condY1 = (not (tempY1 < 0   or   tempY1 > self.maxZoom_verticle))
        condY2 = (not (tempY2 < (self.custom_height - self.maxZoom_verticle)   or   tempY2 > self.custom_height))
        
        
        if  condX1 and condX2 and condY1 and condY2:
            
            self.zoomX1 = tempX1
            self.zoomX2 = tempX2
            self.zoomY1 = tempY1
            self.zoomY2 = tempY2
        
        cx = int((self.zoomX2 - self.zoomX1)/2)
        cy = int((self.zoomY2 - self.zoomY1)/2)
        self.calculate_margins()
        
        
        self.zoomed_img = self.origonal_img.crop((self.zoomX1,self.zoomY1,self.zoomX2,self.zoomY2))#self.interface.zoomX1,self.interface.zoomY1,self.interface.zoomX2,self.interface.zoomY2
        self.zoomed_img = self.zoomed_img.resize((self.custom_width,self.custom_height), Image.NEAREST)
        self.displayImage(self.zoomed_img)
        
    #=======================================================================================================    
    def nextImg(self):
        if self.image_pointer < len(self.img_list)-1:
            print("True")
            self.image_pointer = self.image_pointer + 1
            
            self.loadImage()
        print("next image")
        
        pass
    #=======================================================================================================
    def prevImg(self):
        if self.image_pointer > 0:
            print("True")
            self.image_pointer = self.image_pointer - 1
            
            self.loadImage()
        print("prev image")
        pass
    #=======================================================================================================
    def run(self):
        # while self.thread:
        #     time.sleep(0.05)
        #     self.displayImage(self.zoomed_img)
        # #     #print("IV thread Running")
        pass
            
           
            