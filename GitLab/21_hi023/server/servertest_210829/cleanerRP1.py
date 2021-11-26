import socket
import pymysql
import datetime
from pigpio_dht import DHT11
from pyfirmata import Arduino, util
import time
from threading import Thread
import threading

lock = threading.Lock()

class CleanerRP():
    def __init__(self):
        # 데이터베이스 연결
        self.db = pymysql.connect(host='54.180.136.222',
                                  user='root',
                                  password='haniumhi_023',
                                  db='testdb',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.sensor = DHT11(4) # 온습도 센서 연결
        self.board = Arduino('/dev/ttyACM0') # 아두이노 직렬통신
        self.command_humidity=[] # 살균효과 측정을 위한 스케줄 리스트

        self.thread_flag = False # save_humidityEffect 메소드 스레드 제어

    # 소켓 연결
    def connectSocket(self):
        HOST = '54.180.136.222'
        PORT = 8888
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        name = "STE-0-0000" # 살균기 고유 ID
        self.s.send(name.encode(encoding='utf_8', errors='strict'))

    # 살균
    def clean(self, cleantime):
        self.board.digital[4].write(0) # 가습기 모듈 on
        time.sleep(cleantime)          # cleamtime초동안 살균
        self.board.digital[4].write(1) # 가습기 모듈 off

    # 온도, 습도 측정
    def get_temp_humidity(self):
        result = self.sensor.read() # dht11 센서에서 온습도 측정
        temp_c = result['temp_c'] # 온도값 가져오기
        humidity = result['humidity'] # 습도값 가져오기
        return str(temp_c)+','+str(humidity)

    # 습도 측정
    def get_humidity(self):
        result = self.sensor.read()   # dht11 센서에서 온습도 측정
        humidity = result['humidity'] # 습도값 가져오기
        return str(humidity)

    # 살균효과 지표인 습도 정보 DB서버에 저장
    def save_humidityEffect(self):
        while True:
            if self.thread_flag==True:
                break
            now = datetime.datetime.now()  # 현재 날짜 얻어오기
            formatted_data = now.strftime('%Y-%m-%d %H:%M')  # 현재 시간 문자열 포맷팅
            for i, v in enumerate(self.command_humidity):
                if v['time']==formatted_data:
                    result = self.get_humidity()
                    # save
                    lock.acquire()
                    self.cursor.execute('insert into cleaneffect values(%s,%s,%s)',
                                        (v['cleanid'], v['before'], result))  # 데이터 삽입
                    self.db.commit()
                    lock.release()
                    # delete
                    del self.command_humidity[i]
                    break

    # 살균기 동작 소스 메인
    def run(self):
        self.board.digital[4].write(1) # 릴레이모듈 제어 - 가습기 모듈 off
        t = Thread(target=self.save_humidityEffect) # 살균효과 측정 메소드 스레드
        t.start()
        while True:
            data = self.s.recv(1024)
            if data=="sensor": # 온습도 정보 측정후 서버에 전송
                value = self.get_temp_humidity()
                self.s.send(value.encode(encoding='utf_8', errors='strict'))
            else: # 살균명령
                commad = data.split('-')
                strength = commad[1] # 살균 강도
                cleanid = commad[2] # 살균id
                cleandate = commad[2].split('=')[1] # 살균시간
                date_datetime = datetime.datetime.strptime(cleandate, '%Y-%m-%d %H:%M')
                date = date_datetime + datetime.timedelta(minutes=5) # 살균 5분후에 습도 측정
                date_str = date.strftime('%Y-%m-%d %H:%M')
                before_humidity = self.get_humidity() # 살균 이전 습도 측정
                if strength==0: # 살균강도가 0(하)일 경우
                    self.clean(30)  # 30초 살균
                elif strength==1:   # 살균강도가 1(중)일 경우
                    self.clean(60)  # 1분 살균
                else:               # 살균강도가 2(상)일 경우
                    self.clean(120) # 2분 살균
                command_humidity_dict = dict()
                command_humidity_dict['cleanid'] = cleanid
                command_humidity_dict['before'] = before_humidity
                command_humidity_dict['time'] = date_str
                self.command_humidity.append(command_humidity_dict) # 살균효과 측정을 위한 계획
        self.s.close()
        self.thread_flag = True

cr = CleanerRP()
cr.connectSocket()
cr.run()