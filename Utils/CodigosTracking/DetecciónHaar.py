import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('myhaarF.xml')

# cap = cv2.VideoCapture(0)

#pathVideo = "E:/Fly-Fut/2021-10-16/Moratalaz-SDelPozo/prueba.mp4"
img = cv2.imread("x.jpg")
#cap = cv2.VideoCapture(pathVideo)
#w, h = 1280, 480

while True:
    #ret, img = cap.read()
    h, w, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=9, flags=cv2.CASCADE_SCALE_IMAGE) #myhaar
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        #print(x, " ", y, " ", w, " ", h)
    cv2.imshow('img', img)
    hortizontal_concat = np.concatenate((img, img), axis=1)
    vertical_concat = np.concatenate((img, img), axis=0)

    # cv2.imshow("horizontal", hortizontal_concat)
    # cv2.imshow("vertical", vertical_concat)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
