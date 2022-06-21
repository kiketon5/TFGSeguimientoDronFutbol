import cv2
import numpy as np

(mayor_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


def selectTracker(i):
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
    tracker_types = tracker_types[i]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_types)
    else:
        if tracker_types == 'BOOSTING':
            print("Boosting")
            tracker = cv2.legacy.TrackerBoosting_create()
        if tracker_types == 'MIL':
            print("MIL")
            tracker = cv2.TrackerMIL_create()
        if tracker_types == 'KCF':
            print("KCF")
            tracker = cv2.TrackerKCF_create()
        if tracker_types == 'TLD':
            print("TLD")
            tracker = cv2.legacy.TrackerTLD_create()
        if tracker_types == 'MEDIANFLOW':
            print("MEDIANFLOW")
            tracker = cv2.legacy.TrackerMedianFlow_create()
        if tracker_types == 'CSRT':
            print("CSRT")
            tracker = cv2.TrackerCSRT_create()
        if tracker_types == 'MOSSE':
            print("MOSSE")
            tracker = cv2.legacy.TrackerMOSSE_create()

    return tracker


def YOLODeteccion(img, height, width, counter):
    net = cv2.dnn.readNet('Modelos/yolov3.weights', 'Modelos/yolov3.cfg')
    classes = []

    with open('Modelos/obj.names', 'r') as f:
        classes = f.read().splitlines()
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
    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            ids = np.argmax(score)
            confidence = score[ids]
            if confidence > 0.5:
                center_x = int(detection[0] * width)  # to denoramalize multiplying with original h and w
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_id.append(ids)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            f = open("Resultados/IoU/IoUYoloDetection.csv", "a")
            f.write(str(counter)+","+str(x) + "," + str(y) + "," + str(w) + "," + str(h) + "\n")
            f.close()
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

def selectROI(frame):
    bbox = cv2.selectROI(frame, False)

def HaarDeteccion(img, counter):
    face_cascade = cv2.CascadeClassifier('Modelos/myhaar.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=9, minNeighbors=20, flags=cv2.CASCADE_SCALE_IMAGE)  # myhaarF
    #faces = face_cascade.detectMultiScale(gray, scaleFactor=9, minNeighbors=20, flags=cv2.CASCADE_SCALE_IMAGE)  # myhaar
    if len(faces) != 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            f = open("Resultados/IoU/IoUHaarDetection.csv", "a")
            f.write(str(counter)+","+str(x) + "," + str(y) + "," + str(w) + "," + str(h) + "\n")
            f.close()
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
    #cv2.imshow("IMG", img)


def YOLOSeguimiento(img, height, width):
    net = cv2.dnn.readNet('Modelos/yolov3.weights', 'Modelos/yolov3.cfg')
    classes = []

    with open('Modelos/obj.names', 'r') as f:
        classes = f.read().splitlines()
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
    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            ids = np.argmax(score)
            confidence = score[ids]
            if confidence > 0.5:
                center_x = int(detection[0] * width)  # to denoramalize multiplying with original h and w
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_id.append(ids)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        bbox = [x, y, w, h]
    else:
        # bbox = [3, 1, 2, 2]
        bbox = []
    return bbox, img


def HaarSeguimiento(img):
    face_cascade = cv2.CascadeClassifier('Modelos/myhaar.xml')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # faces = face_cascade.detectMultiScale(gray, scaleFactor=7, minNeighbors=4, flags=cv2.CASCADE_SCALE_IMAGE)  #
    # myhaarF
    faces = face_cascade.detectMultiScale(gray, scaleFactor=9, minNeighbors=20,
                                          flags=cv2.CASCADE_SCALE_IMAGE)  # myhaar
    if len(faces) != 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
        bbox = [x, y, w, h]
    else:
        # bbox = [3, 1, 2, 2]
        bbox = []
    return bbox, img
