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

class CleanerRP():
    def __init__(self):
        pass

    def connectSocket(self):
        HOST = '127.0.0.1'  # '192.168.0.28' #'127.168.111.255'  #'192.168.123.7'
        PORT = 8888
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        name = "STE-9-2222"
        self.s.send(name.encode(encoding='utf_8', errors='strict'))

    def clean(self):
        pass

    def get_f_h(self):
        pass

    def run(self):
        while True:
            data = self.s.recv(1024)
            if data=="exit":
                break
            print(data)
            print("success")

        self.s.close()

cr = CleanerRP()
cr.connectSocket()
cr.run()