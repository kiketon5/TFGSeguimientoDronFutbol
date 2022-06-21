from utils import *
import cv2
import time

w, h = 720, 480
# f = open("IuO.txt", "a")
# f.write(str((w // 2) - 60) + "," + str((h // 2) - 60) + "," + str((w // 2) + 60) + "," + str((h // 2) + 60) + "\n")
# f.close()
centerW = w // 2
centerH = h // 2
pid = [0.25, 0, 0.25]  # Change this to better improve
pError = [0, 0, 0, 0]  # Left-Right, Forward-BackWard, Up-Down, Yaw
startCounter = 0  # for no Fly 1 - for Fly 0
type = 1  # for haarCascade 1 - for SelectROI 0
# myDrone = initializeTello()
start, inicio, tiempo_acc = 0, 0, 0
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

while True:
    if tiempo_acc > 0.32985401153564453:
        myDrone.land()
        myDrone.streamoff()
        False
    # if myDrone.get_battery() < 20:
    #    myDrone.land()
    ## Fly
    inicio = inicio + start
    if startCounter == 0:
        myDrone.takeoff()
        # myDrone.move_up(20)
        startCounter = 1

    ## Step 1
    img = telloGetFrame(myDrone, w, h)

    if type == 0:
        selectROI(img)
        type = 1

    ## Step 2
    img, info = findBall(img, type)
    cv2.circle(img, ((w // 2), (h // 2) - 60), 5, (0, 0, 0), cv2.FILLED)
    # Rectangulo centro del frame
    cv2.rectangle(img, ((w // 2) - 60, (h // 2) - 60), ((w // 2) + 60, (h // 2) + 60), (0, 255, 255), 2)
    # Circulo del centro del frame
    cv2.circle(img, ((w // 2), (h // 2)), 5, (0, 255, 255), cv2.FILLED)

    ##Step 3
    start, final = 0, 0
    start = time.time()
    pError, velocity = trackBall(myDrone, info, w, h, pid, pError)
    final = time.time()
    tiempo_acc += final - start
    f = open("Validacion.csv", "a")
    f.write(str(tiempo_acc) + "," + str(final - start) + "," + str(pError[0]) + "," + str(pError[1]) + "," + str(
        pError[2]) + "," + str(pError[3]) + "," + str(pid[0]) + "," + str(pid[1]) + "," + str(pid[2]) + "," + str(
        velocity[0]) + "," + str(velocity[1]) + "," + str(velocity[2]) + "," + str(velocity[3]) + "\n")
    f.close()
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break
