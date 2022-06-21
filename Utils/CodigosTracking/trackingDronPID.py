import cv2
import numpy as np
from djitellopy import tello
import time

(mayor_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()
me.takeoff()
me.move_up(20)

# ------------------------PARAMETERS----------------------------
widthFrame, heightFrame = 720, 480  # Frame width
centerWFrame = widthFrame // 2
centerHFrame = heightFrame // 2
pid = [0.25, 0, 0.25]  # Constant  of PID proposal, integral, derivated
pError = [0, 0, 0, 0]


def selectTracker():
    tracker = cv2.TrackerKCF_create()
    return tracker


def trackROI(info, w, pid, pError):
    errorX = info[0] - centerWFrame
    errorY = info[1] - centerHFrame
    error = errorX + errorY
    speedLR = 0
    if errorX < -50 or errorX > 50:
        speedLR = pid[0] * errorX + pid[2] * (errorX - pError[0])
        speedLR = int(np.clip(speedLR, -5, 5))

    for_back_velocity = 0
    left_right_velocity = 0
    up_down_velocity = 0
    yaw_velocity = 0
    # Obtain Speed for Yaw velocity
    speedY = pid[0] * errorX + pid[2] * (errorX - pError[0])  # pid[0] = kp, pid[2] = kd
    speedY = int(np.clip(speedY, -100, 100))

    if info[0][0] != 0:  # There is an actual coordinates of ball
        yaw_velocity = speedY
        left_right_velocity = speedLR
        up_down_velocity = 0
        pError = [errorX, 0, errorY, error]
    else:
        for_back_velocity = 0
        left_right_velocity = 0
        up_down_velocity = 0
        yaw_velocity = 0
        speed = 0
        velocity = [0, 0, 0, 0]
        pError = [0, 0, 0, 0]
        
    if me.send_rc_control:
        me.send_rc_control(left_right_velocity, for_back_velocity, up_down_velocity, yaw_velocity)
    return pError


def selectROI(frame, tracker):
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    return ok


def findFace(frame):
    ok, bbox = tracker.update(frame)
    # Draw bounding box
    if ok:
        # Tracking success
        # Inicio y fin del rectangulo
        p1 = [int(bbox[0]), int(bbox[1])]  # Start point
        p2 = [int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])]  # End point

        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        # Center at the middle of the rectangle
        centerXRectangle = (p1[0] + ((p2[0] - p1[0]) // 2))
        centerYRectangle = (p1[1] + ((p2[1] - p1[1]) // 2))
        # Circulo del centro del rectangulo
        cv2.circle(frame, (centerXRectangle, centerYRectangle), 5, (0, 255, 255), cv2.FILLED)
        # Circulo del centro del frame
        cv2.circle(frame, (360, 240), 5, (0, 255, 255), cv2.FILLED)

        # Chequear centro de rectangulo está en el area adecuada
        cv2.rectangle(frame, (310, 190), (410, 290), (0, 255, 0), 2, 1)

    return frame, [centerXRectangle, centerYRectangle]


if __name__ == '__main__':

    frame = me.get_frame_read().frame
    frame = cv2.resize(frame, (widthFrame, heightFrame))
    # Select tracker
    tracker = selectTracker(1)

    # Select bbox of the ROI region
    ok = selectROI(frame, tracker)
    cv2.destroyWindow("ROI selector")

    while True:
        if me.get_battery() < 20:
            me.land()
        frame = me.get_frame_read().frame
        frame = cv2.resize(frame, (widthFrame, heightFrame))

        frame, info = findFace(frame)

        pError = trackROI(info, widthFrame, pid, pError)
        # print(pError)
        # print("Center", info[0], "Area", info[1], "pepe", info)
        cv2.imshow("Output", frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            me.land()
            # cap.release()
            cv2.destroyAllWindows()
            break
