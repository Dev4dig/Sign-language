import cv2
from PIL import Image
import numpy as np

dims =(600,400)

path1 = ''
path2 = r'C:\Users\Adnan Khan\Google Drive\FYP\Sign language\Experiments/h.png'

# img1 = Image.open(path1)

# img1 = np.array(img1)

# img1 = cv2.resize(img1, (dims))



img2 = cv2.imread(path2)
#img2 = cv2.resize(img2, (dims))
print(img2.shape)

#img = cv2.bitwise_and(img1, img2)


cv2.imshow("image", img2)