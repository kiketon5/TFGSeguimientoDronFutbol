from tokenize import Whitespace
from turtle import width
from djitellopy import Tello
import cv2
import numpy as np
import pygame
pygame.init()

def getKey(keyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    #K_{LEFT}
    if keyInput[myKey]:
        ans = True
    pygame.display.update()

    return ans


def telloGetFrame(myDrone, w, h):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img


def YOLO(img, width, height):
    net = cv2.dnn.readNet('Yolo/yolov3.weights', 'Yolo/yolov3.cfg')
    classes = []

    with open('Yolo/obj.names', 'r') as f:
        classes = f.read().splitlines()
    
    blob = cv2.dnn.blobFromImage(img , 1/255 , (416,416) ,(0,0,0) , swapRB = True , crop = False)

    # Set the input into the network
    net.setInput(blob)

    # Get the output layers names
    output_layers_names = net.getUnconnectedOutLayersNames()
    # Put the output layers names into the network
    layerOutputs = net.forward(output_layers_names)

    boxes, confidences, class_id = [], [], []
    myBallsListCenter = []
    myBallsListArea = []
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

    indexes = cv2.dnn.NMSBoxes(boxes,confidences ,0.5,0.4)
    if len(indexes)>0:
        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            return img, [x,y,w,h]
    else:
        return img, [0,0,0,0]

def findFace(img, tracker):
    ok, bbox = tracker.update(img)
    # Draw bounding box
    if ok:
        # Tracking success
        # Inicio y fin del rectangulo
        p1 = [int(bbox[0]), int(bbox[1])]  # Start point
        p2 = [int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])]  # End point
        # Center at the middle of the rectangle
        centerXRectangle = (p1[0] + ((p2[0] - p1[0]) // 2))
        centerYRectangle = (p1[1] + ((p2[1] - p1[1]) // 2))
        return img, [p1, p2, centerXRectangle, centerYRectangle], ok
    return img, [0,0,0,0], ok

def trackBall(myDrone, info, w, h, pid, pError):
    ## PID --> Help moving smoothling not agresive movings
    ## info --> devuelve el centro del rectangulo detectado
    # Obtain the errors in the different axes
    errorX = info[0][0] - w // 2  # centerX - w//2
    errorY = info[0][1] - h // 2
    error = errorX + errorY
    speedLR, speedUD = 0, 0
    
    # Obtain Speed for lateral move
    if errorX < -50 or errorX > 50:
        speedLR = pid[0] * errorX + pid[2] * (errorX - pError[0])
        speedLR = int(np.clip(speedLR, -5, 5))

    # Obtain Speed for Yaw velocity
    speedY = pid[0] * errorX + pid[2] * (errorX - pError[0])  # pid[0] = kp, pid[1] = kd
    speedY = int(np.clip(speedY, -100, 100))

    if info[0][0] != 0:  # There is an actual coordinates of ball
        myDrone.yaw_velocity = speedY
        myDrone.left_right_velocity = speedLR
        myDrone.up_down_velocity = speedUD
        pError = [errorX, 0, errorY, error]
    else:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        myDrone.speed = 0
        pError = [0, 0, 0, 0]

    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity, myDrone.for_back_velocity, myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
    return pError
