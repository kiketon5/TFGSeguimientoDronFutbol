import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('myhaar1.xml')

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("D:/DJI_0007.MP4")

while True:
    ret, img = cap.read()
    img = cv2.resize(img, (720, 480))  # Resize the image to be displayed on the screen

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

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
