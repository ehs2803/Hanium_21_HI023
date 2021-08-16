import time
import socket
import RPi,GPIO as GPIO
from pigpio_dht import DHT11

class CleanerRP():
    def __init__(self):
        self.sensor = DHT11(4)


    def connectSocket(self):
        HOST = '127.0.0.1'  # '192.168.0.28' #'127.168.111.255'  #'192.168.123.7'
        PORT = 8888
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        name = "STE-9-2222"
        self.s.send(name.encode(encoding='utf_8', errors='strict'))

    def clean(self):
        pass

    def get_temp_humidity(self):
        result = self.sensor.read()
        temp_c = result['temp_c']
        humidity = result['humidity']
        return str(temp_c)+','+str(humidity)

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