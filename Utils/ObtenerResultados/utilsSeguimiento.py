import cv2
from utilsFollow import *
import numpy as np
import time
import os


def selectROI(img, modelo, track):
    tracker = selectTracker(track)
    if modelo == 0:
        bbox, img = HaarSeguimiento(img)
    else:
        h, w, _ = img.shape
        bbox, img = YOLOSeguimiento(img, h, w)

    return img, bbox, tracker


def followBall(img, tracker):
    ok, bbox = tracker.update(img)
    # print(ok)
    if ok:
        p1 = [int(bbox[0]), int(bbox[1])]
        p2 = [int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])]
        cv2.rectangle(img, p1, p2, (255, 0, 0), 2, 1)
    return img, ok


def saveFrame(modelo, trackName, counter, img):
    if modelo == 0:
        if not os.path.exists("Fotos/Seguimiento/HaarCorrijoRoi/" + trackName):
            os.makedirs("Fotos/Seguimiento/HaarCorrijoRoi/" + trackName)
        cv2.imwrite("Fotos/Seguimiento/HaarCorrijoRoi/" + trackName + "/" + str(counter) + ".jpg", img)
    else:
        if not os.path.exists("Fotos/Seguimiento/YoloCorrijoRoi/" + trackName):
            os.makedirs("Fotos/Seguimiento/YoloCorrijoRoi/" + trackName)
        cv2.imwrite("Fotos/Seguimiento/YoloCorrijoRoi/" + trackName + "/" + str(counter) + ".jpg", img)


def writerPrueba(timer, modelo, trackName, caja, detecciones):
    if modelo == 0:
        f = open("Resultados/FINALES/Haar" + str(trackName) + ".csv", "w")
    else:
        f = open("Resultados/FINALES/Yolo" + str(trackName) + ".csv", "w")
    for i in range(len(timer)):
        try:
            f.write(str(timer[i]) + ',' + caja[i] + "\n")
        except:
            f.write(str(timer[i]) + "\n")
    f.write(str(detecciones) + "\n")
    f.close()


def detectarMasSeguimiento(modelo, track, trackName):
    cap = cv2.VideoCapture('prueba.mp4')
    timer, caja = [], []
    ok, img = cap.read()
    start = time.time() * 1000
    img, bbox, tracker = selectROI(img, modelo, track)
    tracker.init(img, bbox)
    end = time.time() * 1000
    timer.append(end - start)
    counter = 0
    detecciones = 1
    counter += 1
    ex = True
    while ex:
        x, y, w, h = bbox
        #f = open("Resultados/IoU/IoU" + trackName + ".csv", "a")
        #f.write(str(counter) + "," + str(x) + "," + str(y) + "," + str(w) + "," + str(h) + "\n")
        #f.close()
        caja.append(str(x) + "," + str(y) + "," + str(w) + "," + str(h))
        counter += 1
        start = time.time() * 1000
        ret, img = cap.read()
        #try:
        img, ok = followBall(img, tracker)
        # except:
        #     end = time.time() * 1000
        #     timer.append(end - start)
        #     ex = False
        if not ok:
            end = time.time() * 1000
            timer.append(end - start)
            #saveFrame(modelo, trackName, counter, img)
            # ex = False
            start = time.time() * 1000
            try:
                img, bbox, tracker = selectROI(img, modelo, track)
                while len(bbox) == 0:
                    counter += 1
                    detecciones += 1
                    start = time.time() * 1000
                    img, bbox, tracker = selectROI(img, modelo, track)
                    ret, img = cap.read()
                tracker.init(img, bbox)
            except:
                # end = time.time() * 1000
                # timer.append(end - start)
                ex = False
        end = time.time() * 1000
        timer.append(end - start)
        #saveFrame(modelo, trackName, counter, img)
        #cv2.imshow("img", img)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    # cap.release()
    # cv2.destroyAllWindows()
    timer.append(counter)
    return timer, caja, detecciones
