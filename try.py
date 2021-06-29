import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QImage, QPixmap
import time
import numpy as np
if __name__ == '__main__':
    app = QApplication(sys.argv)
    h, w = 300, 600
    
    for i in range(100):
        time.sleep(2)
        im = np.zeros( (h,w,3), np.uint8)
        for i in range(h):
            for j in range(w):
                for k in range(3):
                    im[i][j][k] = i
        a = QLabel()
        a.resize(w, h)
        # Note the fourth parameter of QtGui.QImage below, which means how many bytes are in each line of the image. If it is not set, the image will sometimes be crooked, so it must be set
        im = QImage(im.data, im.shape[1], im.shape[0], im.shape[1]*3, QImage.Format_RGB888)
        pix = QPixmap(im).scaled(a.width(), a.height())
        a.setPixmap(pix)
    a.show()
    exit(app.exec_())
    
    
    
    
    # def zoom_at(img, x, y, zoom):
    #     w, h = img.size
    #     zoom2 = zoom * 2
    #     img = img.crop((x - w / zoom2, y - h / zoom2, 
    #                 x + w / zoom2, y + h / zoom2))
    # return img.resize((w, h), Image.LANCZOS)