import serial

ser = serial.Serial('COM3',9600, timeout=1)

print("아두이노아 통신 시작")

while True:
    line = ser.readline().decode("utf-8")
    print(line)

