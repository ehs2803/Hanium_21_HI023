import cv2
import numpy as np
import time
import socket
from datetime import datetime

YOLO_net = cv2.dnn.readNet("yolov2-tiny.weights", "yolov2-tiny.cfg")
classes = []
with open("yolo.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

start = time.time()
VideoSignal = cv2.VideoCapture(0)

HOST = '127.0.0.1'  #'192.168.0.28' #'127.168.111.255'  #'192.168.123.7'
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    ret, frame = VideoSignal.read()
    H, W, _ = frame.shape

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
    True, crop=False)
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:

        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * W)
                center_y = int(detection[1] * H)
                dw = int(detection[2] * W)
                dh = int(detection[3] * H)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)

    check=False

    for i in range(len(boxes)):
        if i in indexes:
            if class_ids[i] == 0:
                check=True
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            score = confidences[i]

            x1 = x
            y1 = y
            x2 = x + w
            y2 = y + h
            if x1 < 0: x1 = 0
            if y1 < 0: y1 = 0
            if x2 > W: x2 = W
            if y2 > H: y2 = H

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
            cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5,
                        (255, 255, 255), 1)

    msg=''
    if check==True:
        if time.time()-start>=1:
            now = datetime.now()
            msg = str(1) #now.strftime('%Y=%m-%d %H:%M:%S')+','+
            print(msg)
            s.send(msg.encode(encoding='utf_8', errors='strict'))
            start = time.time()
    else:
        if time.time() - start >= 1:
            now = datetime.now()
            msg = str(0)
            print(msg)
            s.send(msg.encode(encoding='utf_8', errors='strict'))
            start = time.time()

    cv2.imshow("YOLOv3", frame)

    if cv2.waitKey(100) > 0:
        break

VideoSignal.release()
cv2.destroyAllWindows()
time.sleep(1)
s.send("exit".encode(encoding='utf_8', errors='strict'))
s.close()