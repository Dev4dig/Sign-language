
import mediapipe as mp
import threading
import numpy as np

import math
import gestures_module as gm #Gesture module || Self custom
import cv2
from PyQt5 import QtCore
from vs_com_interface import Gestures as g
import vs_com_interface as com
import time


class Detection_Module(QtCore.QThread):
    
    signal_mainPaint = QtCore.pyqtSignal()
    signal_mainIV = QtCore.pyqtSignal()
    signal_IVNext = QtCore.pyqtSignal()
    signal_IVPrev = QtCore.pyqtSignal()
    signal_IVZoom = QtCore.pyqtSignal(int)
     
    #paint signals
    signal_PaintDrawMode = QtCore.pyqtSignal(int, int)
    signal_PaintSelectMode = QtCore.pyqtSignal(int, int)
    signal_PaintClose = QtCore.pyqtSignal()
    
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
        # sc_w, sc_h = autopy.screen.size()

        prev_X, prev_Y = 0,0
        cur_X, cur_Y = 0,0 
        flag = True
        
        last_gesture_right = g.NO_GESTURE
        last_gesture_left = g.NO_GESTURE
        last_zoom = False #whether there was zoom mode in last frame or not
        last_zoom_dist= 0 #last frame zoom distance
        
        while True: 
             
            #dumpImg = np.zeros((720,1280,3))
            success, img = cap.read()
            gesturee = g.NO_GESTURE
            if success:
                img = cv2.flip(img, 1)
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                 
                imgRGB = cv2.resize(imgRGB, (851,650))
                results = self.hands.process(imgRGB)
                
                img = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)
                ih, iw, ic = img.shape
                
                self.interface.camera_view = imgRGB
                if results.multi_hand_landmarks:
                    
                    current_left_gesture = g.NO_GESTURE
                    current_right_gesture = g.NO_GESTURE
                    current_zoom = False
                    current_zoom_dist = 0
                    
                    left_hand = False
                    right_hand = False
                    
                    
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
                        
                        hand_label = com.NO
                        if classification.classification[0].label == "Left":
                            hand_label = com.LEFT_HAND
                            left_hand = True
                        elif classification.classification[0].label == "Right":
                            hand_label = com.RIGHT_HAND
                            self.interface.pointerX = points[self.lms.INDEX_FINGER_TIP].x
                            self.interface.pointerY = points[self.lms.INDEX_FINGER_TIP].y
                            
                            self.interface.drawingX = (points[self.lms.INDEX_FINGER_TIP].x + points[self.lms.THUMB_TIP].x)/2
                            self.interface.drawingY = (points[self.lms.INDEX_FINGER_TIP].y + points[self.lms.THUMB_TIP].y)/2
                            right_hand = True
                        
                        
                        
                        hand = gm.Hand(points, hand_label)
                        total_hands_data.append(hand)#storing hands data for universal use
                        
                        tem_gesture = gm.detect_single_hand_sign(hand)
                        if hand_label == com.RIGHT_HAND:
                            current_right_gesture = tem_gesture
                        elif hand_label == com.LEFT_HAND:
                            current_left_gesture = tem_gesture
                        
                        #displaying label for hand at wrist location
                        cv2.putText(img, str(hand_label), (x,y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
                        
                        
                        
                        #for pixel in xy_pixels:
                            #cv2.putText(img, str(pixel.x), (pixel.x, pixel.y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
                
                    
                    #endfor hand_lms, classification in list(zipped)
                    total_hands = len(total_hands_data)
                    cv2.putText(img, str(total_hands), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                        
                    #decian making part
                    #only make decians if multihand landmarks (mean hands detected)
                    
                    if total_hands ==2:
                        current_zoom, current_zoom_dist = gm.detect_zoom(total_hands_data)
                        gm.draw_distance(p1 = total_hands_data[0].landmarks[self.lms.THUMB_TIP], p2 =total_hands_data[1].landmarks[self.lms.THUMB_TIP], lenth = current_zoom, img = img)
                    #when in paint window
                    if(self.interface.Mode == com.Modes.PAINT_WINDOW):
                        
                        #algorithm
                        if right_hand:
                            if left_hand:
                                #both hands
                                if(current_right_gesture == g.CLICK):
                                    #draw
                                    self.signal_PaintDrawMode.emit(self.interface.drawingX, self.interface.drawingY)
                                    time.sleep(0.001)
                                    print("draw two")
                                    pass
                                elif(current_right_gesture == g.ONE):
                                    #click
                                    if last_gesture_right != g.ONE:
                                        #print("left click")
                                        self.signal_PaintSelectMode.emit(self.interface.pointerX, self.interface.pointerY)
                                    pass
                                elif(current_right_gesture == com.CLOSE_GESTURE and current_left_gesture == com.CLOSE_GESTURE):
                                    #close
                                    if (last_gesture_right != com.CLOSE_GESTURE or last_gesture_left != com.CLOSE_GESTURE):
                                        print("close")
                                        self.signal_PaintClose.emit()
                                    pass
                                pass
                            else:
                                #only ritgt hand
                                if current_right_gesture == g.CLICK:
                                    # #draw
                                    # print("draw single")
                                    # self.signal_PaintDrawMode.emit(self.interface.pointerX, self.interface.pointerY)
                                    self.signal_PaintDrawMode.emit(self.interface.drawingX, self.interface.drawingY)
                                    # time.sleep(0.001)
                                    pass
                                
                                elif current_right_gesture == g.ONE:
                                    if last_gesture_right != g.ONE:
                                        self.signal_PaintSelectMode.emit(self.interface.pointerX, self.interface.pointerY) 
                                    pass
                                pass
                        elif left_hand:
                            #only left hand
                            if current_left_gesture == g.TWO:
                                if last_gesture_left != g.TWO:
                                    #save
                                    print("right save")
                            pass
                        pass
                    
                    #when in main window
                    elif(self.interface.Mode == com.Modes.MAIN_WINDOW):
                        if(current_right_gesture == g.ONE and current_left_gesture != g.ONE):
                            if last_gesture_right != g.ONE:
                                self.signal_mainPaint.emit()
                        elif(current_right_gesture == g.TWO and current_left_gesture != g.TWO):
                            if last_gesture_left != g.TWO:
                                self.signal_mainIV.emit()
                        pass
                    
                    #when in image viewer window
                    elif(self.interface.Mode == com.Modes.IV_WINDOW):
                        if total_hands == 2:
                            #two hands
                            
                            if current_zoom:
                                #zoom mode
                                print("zooming...")
                                if last_zoom:
                                    #zoom in the last frame so send the difference
                                    self.signal_IVZoom.emit(int(current_zoom_dist - last_zoom_dist)) 
                                    pass
                                elif not last_zoom:
                                    #there was no zoom dist in last frame so send dist as zero
                                    self.signal_IVZoom.emit(0)
                                    pass
                                
                                
                                
                                pass
                            elif (current_right_gesture == g.POINTING and current_left_gesture != g.POINTING):
                                #pointing right next
                                if(last_gesture_right != g.POINTING):
                                    self.signal_IVNext.emit()
                                    print("pointing right 2")
                                pass
                            elif (current_right_gesture != g.POINTING and current_left_gesture == g.POINTING):
                                #pointing left...prev
                                if(last_gesture_left != g.POINTING):
                                    self.signal_IVPrev.emit()
                                    print("pointing left 2")
                                pass
                            elif(current_right_gesture == com.CLOSE_GESTURE and current_left_gesture == com.CLOSE_GESTURE):
                                #close
                                if (last_gesture_right != com.CLOSE_GESTURE or last_gesture_left != com.CLOSE_GESTURE):
                                    print("close")
                                pass
                            elif (current_right_gesture == g.POINTING and current_left_gesture == g.POINTING):
                                #both hands are pointing so do nothing
                                pass
                            pass
                        elif total_hands == 1:
                            #one hand
                            if right_hand:
                                #if only right hand
                                if current_right_gesture == g.POINTING:
                                    #pointing right...next
                                    if last_gesture_right != g.POINTING:
                                        self.signal_IVNext.emit()
                                        print("pointing right 1")
                                    pass
                                pass
                            elif left_hand:
                                #left hand only
                                if current_left_gesture == g.POINTING:
                                    #pointing left... prev
                                    if last_gesture_left != g.POINTING:
                                        self.signal_IVPrev.emit()
                                        print("pointing left 1")
                                    pass
                                pass
                            pass
                        pass
                    
                    last_zoom, last_zoom_dist = current_zoom, current_zoom_dist
                    last_gesture_left = current_left_gesture
                    last_gesture_right = current_right_gesture
                    
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








