import vs_com_interface as com
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
from threading import Thread
import cv2
from PyQt5.QtCore import Qt
import numpy as np
import time

class headers:
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    PURPLE = 5

ERASER_MENU = 1
E1 = 2
E2 = 3 
E3 = 4
E4 = 5
E5 = 6
class erasers:
        
    ERASER1 = 5
    ERASER2 = 10
    ERASER3 = 15
    ERASER4 = 20
    ERASER5 = 25

class colors:
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)
    PURPLE = (255,0,255)
    CYAN = (0,255,255)
    

class DrawModes:
    BRUSH = 1
    ERASER = 2
    
class PaintApp(QtWidgets.QWidget):
    
    def __init__(self, i, gesture_thread):
        super().__init__()
        self.interface = i
        self.gesture_thread = gesture_thread
        self.thread = True
        
        
        
        self.height_ = self.interface.CANVAS_H
        self.width_ = self.interface.CANVAS_W
        
        self.brush_thickness = 5
        self.drawing_color = colors.RED #default
        self.eraser_size = 5 #default
        
        self.header_paths = [r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals\red.png',
                            r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals\green.png',
                            r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals\blue.png',
                            r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals\yellow.png',
                            r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals\purple.png']
        
        
        self.eraser_paths = [r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals/erasers.png',
                            r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals/e1.png',
                            r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals/e2.png',
                            r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals/e3.png',
                            r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals/e4.png',
                            r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals/e5.png']
        
        self.eraser_en_path = r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals/eraser-en.png'
        self.camera_en_path = r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals/camera-en.png'
        self.brush_en_path = r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\visuals/brush-en.png'
        
        self.brush_en_img = cv2.imread(self.brush_en_path)
        self.eraser_en_img = cv2.imread(self.eraser_en_path)
        self.camera_en_img = cv2.imread(self.camera_en_path)
        
        
        
        self.header_imgs = [5]
        self.eraser_imgs = [6]
        
        print(len(self.header_imgs))
        print(len(self.eraser_imgs))
        
        for i in self.header_paths:
            print('{i}')
            self.header_imgs.append(cv2.imread(i))
                   
           
            
            
          
        for j in self.eraser_paths:
            print(j)
            self.eraser_imgs.append(cv2.imread(j))
           
        
        # self.eraserSize_img = cv2.imread(self.eraserSize_path)
        # self.header_img = cv2.imread(self.header_path)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        
        #setting app mode to paint 
        self.interface.Mode = com.Modes.PAINT_WINDOW
        self.setWindowTitle("Paint App")
        self.resize(self.width_, self.height_)
        
        self.eraser_menu_backup = np.zeros((285, 78, 3), np.uint8)
        
        self.canvas = QtWidgets.QLabel(self)
        self.canvas.resize(self.width_, self.height_)
        #self.canvas.setStyleSheet("border:2px solid rgb(255, 0,0);")
        
        self.drawing_canvas = np.zeros((self.height_, self.width_, 3), np.uint8)
        
        self.is_webcam = False
        self.eraserSelected = False
        self.is_eraserMenu = False
        self.mode = DrawModes.BRUSH # bursh or eraser ...by default brush
        self.header = self.header_imgs[headers.RED]
    
        
        #registering Events listeners
        self.gesture_thread.signal_PaintDrawMode.connect(self.onDraw)
        self.gesture_thread.signal_PaintSelectMode.connect(self.onSelect)
        self.gesture_thread.signal_PaintClose.connect(self.closeCustom)
        
        self.last_drawingX = 0
        self.last_drawingY = 0
        
        Thread(target=self.run).start()
        
        self.show()
        
    def onDraw(self, x, y):
        
        if y > 60 and y<600:
            if self.mode == DrawModes.BRUSH:
                #draw here
                if self.last_drawingX == 0 and self.last_drawingY == 0:
                    self.last_drawingX = x
                    self.last_drawingY = y
                cv2.line(self.drawing_canvas, (self.last_drawingX, self.last_drawingY), (x, y), self.drawing_color, self.brush_thickness)
                self.last_drawingX = x
                self.last_drawingY = y
            elif self.mode == DrawModes.ERASER:
                cv2.circle(self.drawing_canvas, (self.interface.pointerX,self.interface.pointerY),  self.eraser_size, (0,0,0), cv2.FILLED) #first point green
                pass
            pass
        else:
             #cv2.putText(self.drawing_canvas, "out", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
             pass
        #print(object)
        pass

    def onSelect(self, x, y):
        
        def selectEraser(eraser):
            print(str(eraser))
            self.eraser_size = eraser
            self.is_eraserMenu = False
            self.mode = DrawModes.ERASER 
            
            
        def selectColor(color):
            if self.mode == DrawModes.BRUSH:
                self.drawing_color = color
                if color == colors.RED:
                    self.header = self.header_imgs[headers.RED]
                elif color == colors.GREEN:
                    self.header = self.header_imgs[headers.GREEN]
                elif color == colors.BLUE:
                    self.header = self.header_imgs[headers.BLUE]
                elif color == colors.YELLOW:
                    self.header = self.header_imgs[headers.YELLOW]
                elif color == colors.PURPLE:
                    self.header = self.header_imgs[headers.PURPLE]
                print(str(color))
                
        
        #print("Select mode")
        if (x > 10 and y > 4) and (x < 65 and y <61):
            #red clicked
            selectColor(colors.RED)
            pass
        elif (x > 75 and y > 4) and (x < 128 and y <61):
            # green clicked
            print("green")
            selectColor(colors.GREEN)
            pass
        elif (x > 140 and y > 4) and (x < 193 and y <61):
            # blue clicked
            selectColor(colors.BLUE)
            pass
        elif (x > 205 and y > 4) and (x < 258 and y <61):
            # yellow clicked
            selectColor(colors.YELLOW)
            pass
        elif (x > 270 and y > 4) and (x < 323 and y <61):
            # pruple clicked
            selectColor(colors.PURPLE)
            pass
        
        elif (x > 426 and y > 4) and (x < 474 and y <61):
            # bursh clicked
            print("brush")
            self.mode = DrawModes.BRUSH
            pass
        
        elif (x > 365 and y > 4) and (x < 417 and y <61):
            # camera clicked
            if self.is_webcam:
                self.is_webcam = False
            elif not self.is_webcam:
                self.is_webcam = True
            
            print("camera")
            pass
        elif (x > 615 and y > 4) and (x < 670 and y <61):
            # reset clicked
            print("reset")
            self.drawing_canvas = np.zeros((self.height_, self.width_, 3), np.uint8)
            pass
        
        
        elif (x > 701 and y > 4) and (x < 763 and y <61):
            # eraser clicked
            print("eraser")
            if not self.is_eraserMenu:
                self.is_eraserMenu = True
            elif self.is_eraserMenu:
                self.is_eraserMenu = False
                
            pass
        elif (x > 790 and y > 4) and (x < 840 and y <61):
            # save clicked
            print("save")
            pass
        
        
        #when eraser menu is enabled
        elif self.is_eraserMenu:
            if (x > 692 and y > 61) and (x < 770 and y <101):
                #eraser 1 clicked
                selectEraser(erasers.ERASER1)
                pass
            elif (x > 692 and y > 102) and (x < 770 and y <150):
                #eraser 2 clicked
                selectEraser(erasers.ERASER2)
                pass
            elif (x > 692 and y > 151) and (x < 770 and y <210):
                #eraser 3 clicked
                print("eraser 3 selected")
                selectEraser(erasers.ERASER3)
                pass
            elif (x > 692 and y > 211) and (x < 770 and y <270):
                #eraser 4 clicked
                print("eraser 4 selected")
                selectEraser(erasers.ERASER4)
                pass
            elif (x > 692 and y > 271) and (x < 770 and y <344):
                #eraser 5 clicked
                selectEraser(erasers.ERASER5)
            else:
                #hiding eraser menu if focus out..mean clicked anywhere other than menu
                self.is_eraserMenu = False
                pass
        pass
        
    def closeEvent(self, event):
        print("Window is being closed")
        self.thread = False
        self.interface.Mode = com.Modes.MAIN_WINDOW
        event.accept()
        
    def closeCustom(self):
        print("Window is being closed")
        self.thread = False
        self.interface.Mode = com.Modes.MAIN_WINDOW
        self.close()
    
    def run(self):
        time.sleep(1)
        while self.thread:
            
            time.sleep(0.001)
            image = None
            
            
                     
            
            if self.is_webcam:
                image = self.interface.camera_view
                
            else:
                image = np.zeros((self.height_, self.width_, 3), np.uint8)
            image[0:61, 0:851] = self.header
            #image[61:346, 692:770] = self.eraser_imgs[2]
            
            # if(True):
            #     image[6:344, 690:768] = self.eraserSize_img
            #     image[5:58, 732:794] = self.eraserSize_img
            #image[60:343, 0:76] = self.eraserSize_img
            
            
            
            imgGray = cv2.cvtColor(self.drawing_canvas, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            image = cv2.bitwise_and(image, imgInv)
            image = cv2.bitwise_or(image, self.drawing_canvas)
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            #cv2.line(self.drawing_canvas, (10,10), (self.width_-10, self.height_-10), self.drawing_color, self.brush_thickness)
            #image = self.drawing_canvas
            
            
            #showing eraser menu
            if self.is_eraserMenu:
                image[5:58, 702:764] = self.eraser_en_img
                image[61:346, 692:770] = self.eraser_imgs[2]
             
            if self.mode == DrawModes.BRUSH:
                image[4:57, 426:479] = self.brush_en_img
            elif self.mode == DrawModes.ERASER:
                image[5:58, 702:764] = self.eraser_en_img       
            if self.is_webcam:
                image[4:57, 365:418] = self.camera_en_img         
            #drawing cursor 
            if self.mode == DrawModes.ERASER:
                cv2.circle(image, (self.interface.pointerX,self.interface.pointerY),  self.eraser_size, colors.CYAN, cv2.FILLED)      
            elif self.mode == DrawModes.BRUSH:
                cv2.circle(image, (self.interface.pointerX,self.interface.pointerY),  self.brush_thickness, colors.CYAN, cv2.FILLED) 
                    
            
            ima = QtGui.QImage(image.data, image.shape[1], image.shape[0], image.shape[1]*3, QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap(ima)#.scaled(self.width_, self.height_)
            self.canvas.setPixmap(pix)
            pass