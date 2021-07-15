import cv2
import numpy as np
import math
import mediapipe as mp
from vs_com_interface import Gestures as g
import vs_com_interface as com

mp_hands = mp.solutions.hands
lms = mp_hands.HandLandmark #landmarks constants i.e lms.WRIST
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
drawSpecs = mp_drawing.DrawingSpec(thickness=1, circle_radius=2,)


# Model class for xy pixel pair z is in proportional form not in pixels
class PixelXY:
     def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        
# ========================================
# Model class for hand data
class Hand:
    def __init__(self, landmarks_array, label):
        self.landmarks = landmarks_array
        self.label = label
# ==============================================
#General model class for and array
class Object:
    def __self__(self, data):
        self.data = data
#============================================
# Function for converting proportional values to pixel
def get_pixel_xy(x,y,iw,ih):
    a = int(x*iw)
    b = int(y*ih)
    
    return(a,b)

# ===============================================
# Function for getting all pixel's xy from list of proportional landmarks values¶
#returns an array of objects of PixelXY which contains x y pixel locations for all points
def get_all_xy(handLms, iw, ih):
    xy_pixels = []
    for index, lm in enumerate(handLms):
        x,y = get_pixel_xy(lm.x,lm.y,iw,ih)
        xy_pixels.insert(index, PixelXY(x,y,lm.z)) 
    return xy_pixels
# ======================================================
# Function for drawing distance line and text between two points¶
def draw_distance(p1, p2, lenth, img, direction=''):
    x1 = p1.x
    x2 = p2.x
    y1 = p1.y
    y2 = p2.y
    
    #central points
    cx , cy = (x1+x2) // 2,  (y1+y2) // 2,
   
    
    if direction == 'x':
        cv2.line(img, (x1,cy), (x2,cy), (0,0,255), 1)
        cv2.circle(img, (x1,cy), 5, (0,255,0), cv2.FILLED) #first point green
        cv2.circle(img, (x2,cy), 5, (0,255,255), cv2.FILLED) #second point yellow
        cv2.circle(img, (cx,cy), 5, (255,255,0), cv2.FILLED) #centre point
    
    if direction == 'y':
        cv2.line(img, (cx,y1), (cx,y2), (0,0,255), 1)
        cv2.circle(img, (cx,y1), 5, (0,255,0), cv2.FILLED) #first point green
        cv2.circle(img, (cx,y2), 5, (0,255,255), cv2.FILLED) #second point yellow
        cv2.circle(img, (cx,cy), 5, (255,255,0), cv2.FILLED) #centre point
        
    if direction =='':
        cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 1)
        cv2.circle(img, (x1,y1), 5, (0,255,0), cv2.FILLED) #first point green
        cv2.circle(img, (x2,y2), 5, (0,255,255), cv2.FILLED) #second point yellow
        cv2.circle(img, (cx,cy), 5, (255,255,0), cv2.FILLED) #centre point
    
    cv2.putText(img, str(int(lenth)), (cx,cy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0, 255), 1, cv2.LINE_AA)

    return img


# ======================================================================
# # This function tells whether distance is positive or negetive
# for right hand distance is positive in right direction
# for left hand distance is positive in left direction

def get_distance_sign(x1,x2,y1,y2, hand, orientation):
    dist_sign = ''
    
    #for right hand distance is positive in right direction
    #for left hand distance is positive in left direction
    if hand == com.RIGHT_HAND:
        dist_sign = '+'
    
        if orientation == 'h':
            if x2 < x1:
                dist_sign = '-'
            else:
                if x2 > x1:
                    dist_sign = '+'
        else:
            if orientation == 'v':
                #negetive downward
                if y2 > y1:
                    dist_sign = '-'
                #positive upward
                else:
                    if y2 < y1:
                        dist_sign = '+'
    
    if hand == com.LEFT_HAND:
        dist_sign = '-'

        if orientation == 'h':
            if x2 > x1:
                dist_sign = '-'
            else:
                if x2 < x1:
                    dist_sign = '+'
        else:
            if orientation == 'v':
                if y2 > y1:
                    dist_sign = '-'
                else:
                    if y2 < y1:
                        dist_sign = '+'
    return dist_sign 


# =================================================
# This function gives the distance between two points and draws it if
#draw= True
def distance(p1,p2, orientation = '', hand=''):
    x1 = p1.x
    x2 = p2.x
    y1 = p1.y
    y2 = p2.y
    
     #it cares about left and right hand 
     #for right hand distance is positive in right direction
    #for left hand distance is positive in left direction
    dist_sign = ''
    
    if hand:
        dist_sign = get_distance_sign(x1=x1, x2=x2, y1=y1, y2=y2, hand=hand, orientation=orientation)
    
    lenth = math.hypot(x2-x1, y2-y1)
    text_len = dist_sign+str(int(lenth))
    
    return lenth, dist_sign
    
    # ===============================================
    # Only x distance
    
def distanceX(p1,p2, orientation = 'h', hand=''):
    x1 = p1.x
    x2 = p2.x
    y1 = p1.y
    y2 = p2.y
    
     #it cares about left and right hand 
     #for right hand distance is positive in right direction
    #for left hand distance is positive in left direction
    dist_sign = ''
    
    if hand:
        dist_sign = get_distance_sign(x1=x1, x2=x2, y1=y1, y2=y2, hand=hand, orientation=orientation)
    
    lenth = int(x2-x1)
    text_len = dist_sign+str(int(lenth))
    return np.absolute(lenth), dist_sign

# =================================================
# Only Y distance

def distanceY(p1,p2, orientation = 'v', hand=''):
    x1 = p1.x
    x2 = p2.x
    y1 = p1.y
    y2 = p2.y
    
     #it cares about left and right hand 
     #for right hand distance is positive in right direction
    #for left hand distance is positive in left direction
   
    
    dist_sign = get_distance_sign(x1=x1, x2=x2, y1=y1, y2=y2, hand=hand, orientation=orientation)
    
    lenth = int(y1-y2)
    text_len = dist_sign+str(int(lenth))
    return np.absolute(lenth), dist_sign

#===============================
def check_finger(dip, tip, hand):
    distY, signY = distanceY(dip, tip, hand = hand)
    distX, signX = distanceX(dip, tip, hand = hand)
    
    if distY > distX:
        #when vertical
        if signY == '+':
            return com.FINGER_UP
            
        elif signY == '-':
            #downward/close
            return com.FINGER_DOWN
            
    elif distX > distY:
        #when horizontal
        if signX == '+': # + for in right direction for right hand and + for left hand in left direction
                return com.FINGER_POINTY
        else:
            return com.FINGER_OPPOSITE
    
    #end if            
# =============================================================
def check_thumb(dip,tip, hand):
    distX, signX = distanceX(dip, tip, hand = hand)
    distY, signY = distanceY(dip, tip, hand = hand)
    
    if signX == '+':
        return com.THUMB_CLOSE_H
    elif signX == '-':
        return  com.THUMB_OPEN_H
    # elif distY > distX:
    #     if signX == '+':
    #         return com.THUMB_CLOSE
    #     elif signX == '-':
    #         return  com.THUMB_OPEN
    


#====================:============
# Detect singal hand sign
def detect_single_hand_sign(hand):
    
    gesture = g.NO_GESTURE
    
    label = hand.label
    points = hand.landmarks
    
    
    index_dip = points[lms.INDEX_FINGER_DIP]
    index_tip = points[lms.INDEX_FINGER_TIP]
    
    middle_dip = points[lms.MIDDLE_FINGER_DIP]
    middle_tip = points[lms.MIDDLE_FINGER_TIP]
    
    ring_dip = points[lms.RING_FINGER_DIP]
    ring_tip = points[lms.RING_FINGER_TIP]
    
    pinky_dip = points[lms.PINKY_DIP]
    pinky_tip = points[lms.PINKY_TIP]
    
    thumb_dip = points[lms.THUMB_IP]
    thumb_tip = points[lms.THUMB_TIP]
    
    thumb_ = check_thumb(dip=thumb_dip, tip=thumb_tip, hand = label)
    index_ = check_finger(dip=index_dip, tip=index_tip, hand = label)
    middle_ = check_finger(dip=middle_dip, tip=middle_tip, hand = label)
    ring_ = check_finger(dip=ring_dip, tip=ring_tip, hand = label)
    pinky_ = check_finger(dip=pinky_dip, tip=pinky_tip, hand = label)
    
    dist_tt_it, sign_tt_it = distance(p1 = thumb_tip, p2 = index_tip, hand=label)
    dist_threshold = 45
    if index_ == com.FINGER_UP:
        #index finger is up
        if middle_ == com.FINGER_DOWN and ring_ == com.FINGER_DOWN and pinky_ == com.FINGER_DOWN :
            #one
            return com.Gestures.ONE
            
        elif middle_ == com.FINGER_UP and ring_ == com.FINGER_DOWN and pinky_ == com.FINGER_DOWN :
            #two
            return com.Gestures.TWO
            
        elif middle_ == com.FINGER_UP and ring_ == com.FINGER_UP and pinky_ == com.FINGER_DOWN:
            #three
            return com.Gestures.THREE
            
        elif middle_ == com.FINGER_UP and ring_ == com.FINGER_UP and pinky_ == com.FINGER_UP :
            #four
            return com.Gestures.FOUR
            
        # elif middle_ == com.FINGER_UP and ring_ == com.FINGER_UP and pinky_ == com.FINGER_UP and thumb_ == com.THUMB_OPEN_H:
        #     #fFIVE
        #     return com.Gestures.FIVE
        
            
    elif dist_tt_it < dist_threshold and middle_ == com.FINGER_UP:
        #click
        return com.Gestures.CLICK
    elif index_ == com.FINGER_POINTY and middle_ == com.FINGER_OPPOSITE and ring_ == com.FINGER_OPPOSITE and pinky_ == com.FINGER_OPPOSITE:
        #pointing
        return com.Gestures.POINTING
    elif (pinky_  == com.FINGER_UP and thumb_ == com.THUMB_OPEN_H):
        return com.CLOSE_GESTURE
    
    
    
    # dist_md_mt, sign_md_mt = distanceX(p1=middle_mcp, p2=middle_tip, hand=label )
    # dist_rd_rt, sign_rd_rt = distanceX(p1=ring_mcp, p2=ring_tip, hand=label )
    # dist_pd_pt, sign_pd_pt = distanceX(p1=pinky_mcp, p2= pinky_tip, hand=label )
    
    # dist_id_it, sign_id_it = distanceX(p1=index_mcp, p2=index_tip, hand=label )
    # dist_td_tt, sign_td_tt = distanceX(p1=index_dip, p2=index_tip, hand=label )
    
    # if sign_id_it == '+':
    #     if sign_mm_mt == '-':
    #         if sign_rm_rt == '-':
    #             if sign_pm_pt == '-':
    #                 if label == 'Left':
    #                     gesture = g.POINT_LEFT
    #                 else:
    #                     if label == 'Right':
    #                         gesture = g.POINT_RIGHT
    return gesture
                
# =============================================
# Detects if Zoom mode
def detect_zoom(hands_data):
    index_tip1 = hands_data[0].landmarks[lms.INDEX_FINGER_TIP]
    index_tip2 = hands_data[1].landmarks[lms.INDEX_FINGER_TIP]
                
    thumb_tip1 = hands_data[0].landmarks[lms.THUMB_TIP]
    thumb_tip2 = hands_data[1].landmarks[lms.THUMB_TIP]
                
    
    zoom_dist ,b = distance(p1=index_tip1, p2=index_tip2, orientation='h')
    dist1, sign1 = distance(p1=thumb_tip1, p2=index_tip1)
    dist2, sign2 = distance(p1=thumb_tip2, p2=index_tip2)
    
    
    threshold = 30
    zoom_indicator = False
    
    if dist1 < threshold and dist2 < threshold:
        zoom_indicator = True
    else:
        zoom_indicator = False
    
    return zoom_indicator, zoom_dist