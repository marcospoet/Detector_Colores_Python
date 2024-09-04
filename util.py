import numpy as np
import cv2

def get_limits(color):
    c = np.uint8([[color]]) # aca insertas los valores bgr que queres convertir a hsv
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV) # convertir a hsv
    lower_limit = hsvC[0][0][0] - 10, 100, 100 # limite inferior
    upper_limit = hsvC[0][0][0] + 10, 255, 255 # limite superior

    lower_limit = np.array(lower_limit, dtype=np.uint8) # convertir a array de numpy
    upper_limit = np.array(upper_limit, dtype=np.uint8) # convertir a array de numpy
    return lower_limit, upper_limit