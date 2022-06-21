import cv2
import numpy as np
#from djitellopy import tello
import time

(mayor_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

# me = tello.Tello()
# me.connect()
# print(me.get_battery())

# me.streamon()
# me.takeoff()
# me.send_rc_control(0, 0, 25, 0)
# time.sleep(2.2)

# ------------------------PARAMETERS----------------------------
widthFrame, heightFrame = 720, 480  # Frame width
centerWFrame = widthFrame // 2
centerHFrame = heightFrame // 2
fbRange = [40, 40]  # Area de la pantalla donde se quiere que esté siempre la pelota. A la misma distancia siempre.
fb = 0  # Forward-backward
lr = 0  # Left right
ud = 0  # Up down
pid = [0.4, 0.4, 0]  # Constant  of PID proposal, integral, derivated
pError = 0


def selectTracker(i):
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TDL', 'MEDIANFLOW', 'CSRT', 'MOSSE']
    tracker_types = tracker_types[i]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_types)
    else:
        if tracker_types == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_types == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_types == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_types == 'TDL':
            tracker = cv2.TrackerTDL_create()
        if tracker_types == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_types == 'CSRT':
            tracker = cv2.TrackerCSRT_create()
        if tracker_types == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()

    return tracker

def trackROI(info, w, pid, pError):
    #weight, height = info[1]
    #x, y = info[0]
    errorX = info[2] - centerWFrame
    errorY = info[3] - centerHFrame
    speed = pid[0] * errorX + pid[1] * (errorX - pError)  # proposal * error + derivated * (error - previousError)
    speed = int(np.clip(speed, -100, 100))  # Set speed between -100 and 100

    if errorX > 0:  # Girar a derecha
        # print("Giro a derecha")
        lr = -10
    elif errorX < 0:  # Girar a izquierda
        # print("Giro a izquierda")
        lr = 10
    else: lr = 0  # Centrado horizontalmente

    if errorY > 0:  # Subir el dron
        # print("Subir")
        ud = 10
    elif errorY < 0:  # Bajo el dron
        # print("Bajar")
        ud = -10
    else: ud = 0  # Centrado verticalmente

    # Cuadrar bien la pelota siempre a la misma distancia
    #if weight > fbRange[0] or height > fbRange[1]:  # Area mas grande que 40 hacia atras tiene que ir
        #fb = -10  # Back -> negativo
    #elif height < fbRange[1] or weight < fbRange[0]:
        #fb = 10  # Front -> positivo
    #else:
       # fb = 0
    if ud == 0 and lr == 0: error, speed = 0, 0

    #print("LR: ", lr , " UD: ", ud, " FB: ", fb)
    #    speed = 0
    error = 0
    # print(speed, fb)
    # me.send_rc_control(lr, fb, ud, speed)
    return error

#def selectROI(frame, ok, tracker):
def selectROI(frame, tracker):
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)
 
    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)
    print(bbox)

    # Initialize tracker with first frame and bounding box
    #ok = tracker.init(frame, bbox)
    tracker.init(frame, bbox)

    #return ok

def findFace(frame):
    ok, bbox = tracker.update(frame)
    #print("OK:", ok)
    #print("Bbox: ", bbox)
    # Draw bounding box
    if ok:
        # Tracking success
        p1 = [int(bbox[0]), int(bbox[1])]
        p2 = [int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])]
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        #Center at the middle of the rectangle
        centerXRectangle = (p1[0] + ((p2[0] - p1[0]) // 2))
        centerYRectangle = (p1[1] + ((p2[1] - p1[1]) // 2))
        cv2.circle(frame, (centerXRectangle, centerYRectangle), 5, (0, 255, 255), cv2.FILLED)
        #Circle of center of the frame
        cv2.circle(frame, (360,240), 5, (0, 255, 255), cv2.FILLED)

        return frame, [p1, p2, centerXRectangle, centerYRectangle]
    else:
        return frame, [[0,0], [0,0], 0, 0]


if __name__ == '__main__':
    
    cap = cv2.VideoCapture(0)
    ok, frame = cap.read()

    #Select tracker
    tracker = selectTracker(2)

    #Select bbox of the ROI region
    #ok = selectROI(frame, ok, tracker)
    selectROI(frame, tracker)
    #print(ok)
    cv2.destroyWindow("ROI selector")

    while True:
        ok, frame = cap.read()
        frame = cv2.resize(frame, (widthFrame, heightFrame))
        
        frame, info = findFace(frame)
        pError = trackROI(info, widthFrame, pid, pError)
        # print(pError)
        # print("Center", info[0], "Area", info[1], "pepe", info)
        cv2.imshow("Output", frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            #me.land()
            
            cap.release()
            cv2.destroyAllWindows()
            break
