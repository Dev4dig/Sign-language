
from threading import Thread
import time


class Modes:
    MAIN_WINDOW = 1
    PAINT_WINDOW = 2
    IV_WINDOW = 3 # IMAGE VIEWER IV
    GESTURE_WINDOW = 4
    
class Gestures:
    ONE = 21
    TWO = 22
    THREE = 33
    FOUR = 24
    FIVE = 25
    CLICK = 26
    ZOOM_MODE = 27
    DRAW_MODE = 28
    POINT_LEFT = 29
    POINT_RIGHT = 30
    SAVE = 31
    CLOSE = 32
    NO_GESTURE = 0
    
 
        
        
 

class Com_interface:
    def __init__(self):
        #signals from App to Gesture Algorithm/module/thread
        self.Mode = 0 # no mode
        self.Zoom = True
        #colors: red 239,3,3 green 23,174,3 blue 0,0,253  black 0,0,0 ywllow 255, 255,0
        self.CANVAS_H = 650
        self.CANVAS_W = 850

        self.zoomX1 = 1
        self.zoomY1 = 1
        self.zoomX2 = 699
        self.zoomY2 = 699   
        
    
        
        
        #signals from Gesture Algorithm/module/thread to App 
        self.i = 0
       
    def setCurrentMode(self, mode):
        self.Mode = mode
   
    
    
    