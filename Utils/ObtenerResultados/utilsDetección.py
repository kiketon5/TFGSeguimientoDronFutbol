import cv2
import numpy as np
import time
import os
from utilsFollow import *


def detection(modelo):
    cap = cv2.VideoCapture('prueba.mp4')  # For webcam put 0
    counter = 0
    timer = []
    while True:
        ret, img = cap.read()
        cv2.resize(img, (240,480), interpolation=cv2.INTER_AREA)
        if not ret: break
        counter += 1
        h, w, _ = img.shape
        if modelo == 0:
            start = time.time() * 1000
            HaarDeteccion(img, counter)
            end = time.time() * 1000
            timer.append(end - start)
        if modelo == 1:
            start = time.time() * 1000
            YOLODeteccion(img, h, w, counter)
            end = time.time() * 1000
            timer.append(end - start)
        if modelo == 2:
            start = time.time() * 1000
            selectROI(img)
            # YOLODeteccion(img, h, w, counter)
            end = time.time() * 1000
            timer.append(end - start)
            print(end-start)

        cv2.imwrite("Fotos/SelectROI/" + str(counter) + ".jpg", img)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    timer.append(counter)
    cap.release()
    cv2.destroyAllWindows()
    return timer

def writePrueba(timer, modelo):
    if modelo == 0:
        f = open("Resultados/DeteccionHaar.csv", "w")
    if modelo == 1:
        f = open("Resultados/DeteccionYolo.csv", "w")
    if modelo == 2:
        f = open("Resultados/DeteccionSelectROI.csv", "w")
    for i in range(len(timer)):
        f.write(str(timer[i]) + "\n")
    f.close()

def accuracy():
    contenido = [file for file in os.listdir("Fotos/Seguimiento/YoloCorrijoRoi/MEDIANFLOW") if (file.endswith('.jpg'))]
    TP = [file for file in os.listdir("Fotos/Seguimiento/YoloCorrijoRoi/MEDIANFLOW/TP") if (file.endswith('.jpg'))]
    for img in contenido:
        #print(img)
        if img in TP:
            #print(img)
            os.remove("Fotos/Seguimiento/YoloCorrijoRoi/MEDIANFLOW/" + img)


