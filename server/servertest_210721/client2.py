import cv2
import numpy as np
import time
import socket
from datetime import datetime



start = time.time()

HOST = '127.0.0.1'  #'192.168.0.28' #'127.168.111.255'  #'192.168.123.7'
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

name = "NO20210722"
s.send(name.encode(encoding='utf_8', errors='strict'))
check=True
while True:
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

    if cv2.waitKey(100) > 0:
        break

s.send("exit".encode(encoding='utf_8', errors='strict'))
s.close()