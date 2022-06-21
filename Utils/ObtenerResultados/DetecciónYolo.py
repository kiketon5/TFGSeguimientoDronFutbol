import cv2
import numpy as np

# https://www.youtube.com/watch?v=1LCb1PVqzeY

net = cv2.dnn.readNet('Yolo/yolov3.weights', 'Yolo/yolov3.cfg')
classes = []

with open('Yolo/obj.names', 'r') as f:
    classes = f.read().splitlines()

#cap = cv2.VideoCapture('E:/Fly-Fut/2021-10-16/Moratalaz-SDelPozo/prueba.mp4') #For webcam put 0
img = cv2.imread('x.jpg')

while True:
    #_, img = cap.read()
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img , 1/255 , (416,416) ,(0,0,0) , swapRB = True , crop = False)

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

    indexes = cv2.dnn.NMSBoxes(boxes,confidences ,0.5,0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    #colors = np.random.uniform(0,255,size=(len(boxes), 3))
    if len(indexes)>0:
        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            label = str(classes[class_id[i]])
            confi = str(round(confidences[i],2))
            #color = colors[i]
            cv2.rectangle(img , (width//2,0) , (width//2+w,height) , (0,0,255) ,2)
            cv2.rectangle(img , (x,y) , (x+w,y+h) , (255,0,0) ,2)
            cv2.circle(img, (x,y), 2, (0,255,255), cv2.FILLED)
            #cv2.putText(img , label +" "+confi , (x,y+20) ,font ,2 ,(255,255,255),2)
    #cv2.imshow("Frame" , img)
    cv2.imwrite("prediccion.jpg", img)
    key = cv2.waitKey(1)
    if key==27:#ESC key
        break
#cap.release()
cv2.destroyAllWindows()
