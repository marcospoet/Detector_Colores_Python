import cv2
from PIL import Image
from util import get_limits
import numpy as np


yellow = [0, 255, 255] # color amarillo en bgr
red = [0, 0, 255] # color rojo en bgr
blue = [255, 0, 0] # color azul en bgr
celeste = [255, 255, 0] # color celeste en bgr
cap = cv2.VideoCapture(0) # 0 es el id de la camara

color_elegido = red

while True:
    ret,frame = cap.read() # leer un frame y el retorno

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convertir el frame a hsv
    
    if color_elegido != red:
        lower_limit, upper_limit = get_limits(color=color_elegido) # obtener los limites inferior y superior del color amarillo
        mask = cv2.inRange(hsvImage,lower_limit,upper_limit) # aplicar la mascara al frame
    else:
        redBajo1 = np.array([0,100,20],np.uint8)
        redAlto1 = np.array([8,255,255],np.uint8)
        maskRed1 = cv2.inRange(hsvImage, redBajo1, redAlto1) #esto se hace porque el rojo aparece en las dos puntas del circulo de colores
        redBajo2 = np.array([175,100,20],np.uint8)
        redAlto2 = np.array([179,255,255],np.uint8)
        maskRed2 = cv2.inRange(hsvImage, redBajo2, redAlto2)
        mask = cv2.add(maskRed1, maskRed2) #aplico las dos mascaras juntas en una sola
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 3000:
            M=cv2.moments(c) #calcular los momentos de la imagen
            if (M["m00"]==0): M["m00"]=1 #evitar division por cero
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1) #dibujar un circulo en el centro del objeto
            font=cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA) #mostrar coordenadas
            new_contour = cv2.convexHull(c) #me suaviza el contorno
            cv2.drawContours(frame, [new_contour], 0, (0, 255, 0), 3)


    maskredvis = cv2.bitwise_and(frame, frame, mask=mask) # esto es para que se vea el color que se esta detectando en la mascara
    cv2.imshow('mask-con-Color',maskredvis) # mostrar la mascara #sirve para ver como se muestra la mascara, tipo te pone los pixeles que queres
    
    cv2.imshow('frame',frame) # mostrar el frame

    if cv2.waitKey(1) & 0xFF == ord('q'): # si se presiona la tecla q se cierra
        break

cap.release() # liberar la camara
cv2.destroyAllWindows() # destruir todas las ventanas
