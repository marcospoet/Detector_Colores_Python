import cv2
from PIL import Image
from util import get_limits
import numpy as np

yellow = [0, 255, 255] # color amarillo en bgr
red = [0, 0, 255] # color rojo en bgr
blue = [255, 0, 0] # color azul en bgr
celeste = [255, 255, 0] # color celeste en bgr
cap = cv2.VideoCapture(0) # 0 es el id de la camara

color_elegido = celeste

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
    
    mask_ = Image.fromarray(mask) # convertir la mascara a imagen de PIL, no hace nada mas, tipo convierte el array de numpy 

    bbox = mask_.getbbox() # obtener el bounding box de la mascara, es asi de facil porque uso pil 

    if bbox: # si hay un bounding box
        x1, y1, x2, y2 = bbox # obtener las coordenadas del bounding box
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5) # dibujar el bounding box en el frame
    
    print(bbox) # imprimir el bounding box

    cv2.imshow('mask',mask) # mostrar la mascara #sirve para ver como se muestra la mascara, tipo te pone los pixeles que queres
    
    cv2.imshow('frame',frame) # mostrar el frame

    if cv2.waitKey(1) & 0xFF == ord('q'): # si se presiona la tecla q se cierra
        break

cap.release() # liberar la camara
cv2.destroyAllWindows() # destruir todas las ventanas


"""
dato de color:
La función cv2.waitKey(1) de OpenCV espera una entrada de teclado y devuelve un valor entero de 32 bits que representa el código Unicode de la tecla presionada.
Sin embargo, en la mayoría de los casos, solo estamos interesados en los 8 bits menos significativos de este valor, que es donde se almacena el código ASCII de la tecla presionada.
Por lo tanto, para extraer este valor, aplicamos la operación AND bit a bit con 0xFF, que es un número de 8 bits que tiene todos los bits establecidos en 1.
Esta operación tiene el efecto de "enmascarar" todos los bits del valor devuelto por cv2.waitKey(1) excepto los 8 bits menos significativos.
Por lo tanto, cv2.waitKey(1) & 0xFF nos da el código ASCII de la tecla presionada. Luego, comparamos este valor con ord('q'), que es el código ASCII de la tecla 'q', para ver si la tecla 'q' fue la que se presionó.

"""
