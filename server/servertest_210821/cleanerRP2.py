import cv2
import numpy as np
import time
import socket
from datetime import datetime
import keyboard
import pigpio

#pwm_pin = 18
#pi = pigpio.pi()
#pi.set_mode(pwm_pin, GPIO.OUTPUT)
#angle = 0
#pi.set_servo_pulsewidth(pwm_pin, angle * 100 + 500)


start = time.time()

HOST = '127.0.0.1'
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

name = "STE2222"
s.send(name.encode(encoding='utf_8', errors='strict'))

while True:
    data=s.recv(1024)
    print(data)
    if data=="clean":
        # 온습도센서 결과
        # pi.set_servo_pulsewidth(pwm_pin, angle * 100 + 500)
        # 온습도 센서
        s.send("cleanResult:info".encode(encoding='utf_8', errors='strict'))


s.send("exit".encode(encoding='utf_8', errors='strict'))
s.close()