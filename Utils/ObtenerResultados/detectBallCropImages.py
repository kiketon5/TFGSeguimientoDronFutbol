import cv2
import numpy as np
import os
import shutil


# https://www.youtube.com/watch?v=1LCb1PVqzeY


def detectBall(img, height, width):
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

    # Set the input into the network
    net.setInput(blob)

    # Get the output layers names
    output_layers_names = net.getUnconnectedOutLayersNames()
    # Put the output layers names into the network
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_id = []
    infoHaar = []
    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            ids = np.argmax(score)
            confidence = score[ids]
            if confidence > 0.80:
                center_x = int(detection[0] * width)  # to denoramalize multiplying with original h and w
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                # infoYolo = [detection[0], detection[1], detection[2], detection[3]]
                infoHaar = [x - 7, y - 7, w + 7, h + 7]
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_id.append(ids)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    # colors = np.random.uniform(0,255,size=(len(boxes), 3))
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_id[i]])
            confi = str(round(confidences[i], 2))
            # color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return img, infoHaar


def YOLO(x1, y1, w, h, dw, dh):
    x1 = float((x1 + w + x1) / 2) / dh
    y1 = float((y1 + h + y1) / 2) / dw
    x2 = float(w / dh)
    y2 = float(h / dw)
    return x1, y1, x2, y2


def guardarTxtYolo(info):
    img = imagen[:-4]
    directory = "E:/pictures/prueba/lYolo/" + img + ".txt"
    f = open(directory, "w")
    info = "0 " + str(info[0]) + " " + str(info[1]) + " " + str(info[2]) + " " + str(info[3])
    f.write(info)
    f.close


def guardarTxtHaar(info):
    img = imagen[:-4]
    directory = "E:/pictures/prueba/lHaar/" + img + ".txt"
    f = open(directory, "w")
    info = "1 " + str(info[0]) + " " + str(info[1]) + " " + str(info[2]) + " " + str(info[3])
    f.write(info)
    f.close


if __name__ == "__main__":

    directory = 'E:/pictures/'
    # Imagenes que serán analizadas.
    contenido = [file for file in os.listdir(directory + 'PruebaNoBall') if
                 (file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.png') or file.endswith('.jpeg'))]

    net = cv2.dnn.readNet('Yolo/yolov3.weights', 'Yolo/yolov3.cfg')
    classes = []

    with open('Yolo/obj.names', 'r') as f:
        classes = f.read().splitlines()

    # con = 0
    initial_count = 0
    for path in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, path)): initial_count += 1
    print(initial_count)

    for imagen in contenido:
        # print(imagen)
        # Imagen a analizar.
        img = directory + 'PruebaNoBall/' + imagen
        img = cv2.imread(img)
        height, width, _ = img.shape
        img, infoHaar = detectBall(img, height, width)
        if infoHaar != []:
            infoYolo = YOLO(infoHaar[0], infoHaar[1], infoHaar[2], infoHaar[3], width, height)
            guardarTxtYolo(infoYolo)
            guardarTxtHaar(infoHaar)
            shutil.move(directory + 'PruebaNoBall/' + imagen, directory + 'prueba/img/' + imagen)
        else:
            shutil.move(directory + 'PruebaNoBall/' + imagen, directory + 'prueba/mal/' + imagen)
        # con += 1
        # print(initial_count - con)
        # cv2.imshow("Frame", img)
        # cv2.waitKey(0)
