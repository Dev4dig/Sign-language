
import mediapipe as mp
import threading
import numpy as np
import autopy
import math
import gestures_module as gm #Gesture module || Self custom
import cv2
from PyQt5 import QtCore
from vs_com_interface import Gestures as g
import vs_com_interface as com


class Detection_Module(QtCore.QThread):
    
    signal_mainPaint = QtCore.pyqtSignal()
    signal_mainIV = QtCore.pyqtSignal()
    signal_IVNext = QtCore.pyqtSignal()
    signal_IVPrev = QtCore.pyqtSignal()
    signal_IVZoom = QtCore.pyqtSignal(int,int,int,int)
     
    #paint signals
    signal_PaintDrawMode = QtCore.pyqtSignal(int, int, object)
    signal_PaintSelectMode = QtCore.pyqtSignal(int, int)
    
    def __init__(self, c, parent=None):
        super(Detection_Module,self).__init__(parent)
        self.i= 0
        self.interface = c
        
        self.mp_hands = gm.mp_hands
        self.lms = gm.lms
        self.hands = gm.hands
        self.mp_drawing = gm.mp_drawing
        self.drawSpecs = gm.drawSpecs
        pass
    #end __init__()
    
    
    
    def draw_connections(self, img, hand_lms):
        self.mp_drawing.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS, 
                                            self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=3, circle_radius=5),
                                            self.mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                            )
        return img
    
    def run(self):
        cap = cv2.VideoCapture(0)
        sc_w, sc_h = autopy.screen.size()

        prev_X, prev_Y = 0,0
        cur_X, cur_Y = 0,0 
        flag = True

        while True: 
            
            #dumpImg = np.zeros((720,1280,3))
            success, img = cap.read()
            gesturee = g.NO_GESTURE
            if success:
                img = cv2.flip(img, 1)
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                 
                imgRGB = cv2.resize(imgRGB, (850,650))
                results = self.hands.process(imgRGB)
                
                img = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)
                ih, iw, ic = img.shape
                 
                if results.multi_hand_landmarks:
                    total_hands_data = [] #array of Hand objects contains data about all the hands in the frame

                    #custom code       
                    zipped = zip(results.multi_hand_landmarks,results.multi_handedness)
                    
                    #FOR LOOPING THROUGH TOTAL NUMBER OF HANDS
                    for hand_lms, classification in list(zipped):
                        
                        #rendering connections
                        img = self.draw_connections(img, hand_lms)
                        
                        points = gm.get_all_xy(hand_lms.landmark, iw, ih)
                        
                        # Wrist XY
                        x = points[self.lms.WRIST].x
                        y = points[self.lms.WRIST].y
                        hand_label = classification.classification[0].label
                        
                        total_hands_data.append(gm.Hand(points, hand_label))#storing hands data for universal use
                        
                        #displaying label for hand at wrist location
                        cv2.putText(img, hand_label, (x,y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
                        
                        
                        #dist,sign, img = distance(p1=points[lms.THUMB_TIP], p2=points[lms.INDEX_FINGER_TIP], orientation='v', img=img, draw=True, hand = hand_label)
                        #drawing verticle line on hands
                        hand_hight, s = gm.distance(p1=points[self.lms.WRIST], p2=points[self.lms.MIDDLE_FINGER_TIP], orientation='v', hand = hand_label)
                        gm.draw_distance(p1=points[self.lms.WRIST], p2=points[self.lms.MIDDLE_FINGER_TIP], lenth = hand_hight, img = img)
                        
                        #for pixel in xy_pixels:
                            #cv2.putText(img, str(pixel.x), (pixel.x, pixel.y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
                
                    
                    #endfor hand_lms, classification in list(zipped)
                    total_hands = len(total_hands_data)
                    cv2.putText(img, str(total_hands), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    if total_hands == 1:
                        #single hand
                        gesture = gm.detect_single_hand_sign(total_hands_data)
                        cv2.putText(img, str(gesture), (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
                        gesturee = gesture
                    if total_hands == 2:
                        #drawing middle tip to tip distance for debugging
                        #a,b = gm.distance(p1=total_hands_data[0].landmarks[self.lms.INDEX_FINGER_TIP], p2=total_hands_data[1].landmarks[self.lms.INDEX_FINGER_TIP], orientation='h', hand = hand_label)
                        
                        zoom_indicator, zoom_level = gm.detect_zoom(total_hands_data)
                        
                        if zoom_indicator:
                            cv2.putText(img, "zoom mode: "+str(int(zoom_level)), (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
                            gm.draw_distance(p1=total_hands_data[0].landmarks[self.lms.INDEX_FINGER_TIP], p2=total_hands_data[1].landmarks[self.lms.INDEX_FINGER_TIP], img=img, lenth = zoom_level)
                            
                                    
                        
                    #decian making part
                    #only make decians if multihand landmarks (mean hands detected)
                    if(self.interface.Mode == com.Modes.MAIN_WINDOW):    
                        if gesturee == g.POINT_RIGHT:
                            self.signal_mainPaint.emit()
                        elif gesturee == g.POINT_LEFT:
                            self.signal_mainIV.emit()
                    elif(self.interface.Mode == com.Modes.IV_WINDOW):
                        pass
                    #multihand landmarks body
                #endif multilandmarks   
                
                cv2.imshow("image", img)
                        
            #endif success
            #one frame processing ends 
            else: #if no frame detected
                print("failed")

        
            cv2.waitKey(1)
        
        
        
        
            #end While body
        #end While scope
    #end run
#end Detection module class


# a = Detection_Module(1)
# a.run()








