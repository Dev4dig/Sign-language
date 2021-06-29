import cv2
import matplotlib.pyplot as plt
import os
import time
from threading import Thread
from queue import Queue
import cv2

import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel
import sys
 
 
 

dim = (2000, 2000) #w,h
path = r'C:\Users\Adnan Khan\Google Drive\FYP\d.JPG'
img = cv2.imread(path)  #h,w,channel

resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
cv2.imwrite("img_name.jpg", resized)
win_frame_w = 600
win_frame_h = 500
window_frame = np.zeros((win_frame_h, win_frame_w, 3), np.uint8) # h,w,channels
start_x = int((resized.shape[1]-win_frame_w)/2)
start_y = int((resized.shape[0]-win_frame_h)/2)
for height in range(win_frame_h):
    for width in range(win_frame_w):
        for channel in range(3):
            window_frame[height][width][channel]= resized[height+start_y-1][width+start_x-1][channel] 

ima = QImage(window_frame.data, window_frame.shape[1], window_frame.shape[0], window_frame.shape[1]*3, QImage.Format_RGB888)

app = QApplication(sys.argv)


a = QLabel()
a.resize(win_frame_w,win_frame_h)
# Note the fourth parameter of QtGui.QImage below, which means how many bytes are in each line of the image. If it is not set, the image will sometimes be crooked, so it must be set
pix = QPixmap(ima).scaled(a.width(), a.height())
a.setPixmap(pix)
a.show()
exit(app.exec_())