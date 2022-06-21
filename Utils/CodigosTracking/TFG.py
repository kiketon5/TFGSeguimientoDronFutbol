from utils import *
import cv2
import time

w, h = 720, 480
centerW = w // 2
centerH = h // 2
pid = [0.25, 0, 0.25]  # Change this to better improve
pError = [0, 0, 0, 0]  # Left-Right, Forward-BackWard, Up-Down, Yaw
startCounter = 0 # leave it 0

def Seguimiento(img, tracker):
    if myDrone.get_battery() < 15:
            myDrone.land()
            myDrone.streamoff()
            det = False
            return det
    ## Step 1
    img, info, ok = findFace(img, tracker)    
    if ok == False:
        seg = False
        return seg
    ##Step 3
    pError = trackBall(myDrone, info, w, h, pid, pError)
    
    

if __name__ == '__main__':
    # Initialize Dron Values
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    mover, battery, seg, det = True, True, True, True

    ## Fly
    if startCounter == 0:
        myDrone.takeoff()
        while mover:
            if getKey("UP"):
                myDrone.move_up(10)
            if getKey("a"):
                mover = False
        startCounter = 1
    while det:
        ## Step 1
        img = telloGetFrame(myDrone, w, h)
        # Deteccion
        img, bbox = YOLO(img, w, h)
        tracker = cv2.TrackerKCF_create()
        ok = tracker.init(img, bbox)
        while seg:
            det = Seguimiento(img, tracker)
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                myDrone.land()
                break
