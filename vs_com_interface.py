
from threading import Thread
import time


class Modes:
    MAIN_WINDOW = 1
    PAINT_WINDOW = 2
    IV_WINDOW = 3 # IMAGE VIEWER IV
    
    GV_WINDOW = 4
    
    
class Gestures:
    ONE = 21
    TWO = 22
    THREE = 23
    FOUR = 24
    FIVE = 25
    CLICK = 26
    ZOOM_MODE = 27
    DRAW_MODE = 28
    POINTING = 29
    POINT_RIGHT = 30
    SAVE = 31
    CLOSE = 32
    NO_GESTURE = 0
    SELECTION_CLICK = 55
    
    

FINGER_UP = 40
FINGER_DOWN = 41
FINGER_RIGHT = 42
FINGER_LEFT = 43
FINGER_POINTY = 44
FINGER_OPPOSITE = 45
THUMB_OPEN_H = 46  #horizontal
THUMB_CLOSE_H = 47 #horizontal
THUMB_CLOSE_V = 48 #VERTICAL
THUMB_OPEN_V = 49 #VERTICAL
NO = 0  
RIGHT_HAND = 51
LEFT_HAND = 52
CLOSE_GESTURE = 53
HAND_CLOSE = 56
        
        
 

class Com_interface:
    def __init__(self):
        #signals from App to Gesture Algorithm/module/thread
        self.Mode = 0 # no mode
        self.Zoom = True
        #colors: red 239,3,3 green 23,174,3 blue 0,0,253  black 0,0,0 ywllow 255, 255,0
        self.CANVAS_H = 650
        self.CANVAS_W = 851

        self.pointerX = 1
        self.pointerY = 1
         
        self.drawingX = 0
        self.drawingY = 0
        self.camera_view = None
    
        self.zoom_centerX = 0
        self.zoom_centerY = 0
        
        #signals from Gesture Algorithm/module/thread to App 
        self.i = 0
       
    def setCurrentMode(self, mode):
        self.Mode = mode
   
    
    
    