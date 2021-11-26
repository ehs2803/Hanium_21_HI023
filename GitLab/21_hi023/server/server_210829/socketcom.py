import socket
import pymysql
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread
import threading
import os
import json

lock = threading.Lock()

class Socket():
    def __init__(self):
        # 데이터베이스 연결
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='1234',
                                  db='testdb',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        # 카메라, 분부기 등록 날짜
        self.registerDate= datetime.datetime.now()
        # 인공지능 기반 살균 시작 날짜
        self.startDate = (self.registerDate+ datetime.timedelta(days=2)).strftime('%Y=%m-%d')
        self.CAMlist=[]  # 카메라 라즈베리파이 고유 아이디 등록
        self.STElist=[]  # 살균기 라즈베리파이 고유 아이디 등록
        self.sched = BackgroundScheduler(timezone="Asia/seoul")
        self.sched.add_job(self.cleanAlgorithm, 'cron', hour=0)  # 인공지능 살균 스케줄러

        self.fiveMin_data=[] # [ [0,1,1,0,0 ...], [1,1,0,0,0,...] ]
        self.fiveMin_data_dict= []  # [ {'00:00':0, '00:05':1 ...}, ... ]
        self.cleantime=[]  # 살균시간 저장 [ ['09:20', '16:20'], ['10:10', '12:30', '15:30'] ]
        self.cleanstrength=[] # 상:2 중:1 하:0

        self.cid = ''
        self.ccheck = False
        self.cmd = ''

        self.sensorCheck = False
        self.sensorValue=[]

    # 검증필요
    def get_connectedDevice(self):
        list=[]
        connectedDevice_dict = dict()
        for i, v in enumerate(self.CAMlist):
            connectedDevice_dict['type']='camera'
            connectedDevice_dict['id']=v[0]
            connectedDevice_dict['name']=v[1]
            list.append(connectedDevice_dict)
            connectedDevice_dict['type'] = 'cleaner'
            connectedDevice_dict['id'] = self.STElist[i]
            connectedDevice_dict['name'] = v[1]
        return list

    def get_roomName(self):
        list=[]
        for i in self.CAMlist:
            list.append(i[1])
        return list

    def get_STEID(self):
        return self.STElist

    def get_sensor_value(self):
        list_value=[]
        for i in self.STElist:
            self.cid = i
            self.ccheck = True
            self.cmd = "sensor"
            if self.sensorCheck==True:
                self.sensorCheck=False
                temp=self.sensorValue
            list_value.append(temp)
        return list_value

    def json_default(self, value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d %H:%M:%S')

    def get_effect(self):
        self.cursor.execute("SELECT name, time, cleaneffect.before, after FROM cleandata, cleaneffect "
                            "WHERE cleandata.cleanid=cleaneffect.cleanid order by time desc")
        data = json.dumps(self.cursor.fetchall(), default=self.json_default)
        return data

    def get_document(self):
        self.cursor.execute("SELECT name, time, way, strength FROM cleandata order by time desc")
        data = json.dumps(self.cursor.fetchall(), default=self.json_default)
        return data

    # 인공지능 기반 살균 알고리즘
    def cleanAlgorithm(self):
        # 학습데이터 검증
        self.verificationData()

        # 전처리 - 5분단위로
        self.make_fiveMin()

        # 5분 단위 저장
        self.save_fivemin()

        # 전처리 - 딕셔너리 형태로
        self.make_dict()


        # 받아온 학습결과기반 살균 알고리즘
        for i in self.fiveMin_data_dict:
            result = self.algorithms(i)
            self.cleantime.append(result)

        # 군집화


        # 살균알고리즘 기반 살균 시간 저장
        self.save_cleantime()

    def algorithms(x):
        # 살균 알고리즘의 아이디어는 sin, cos함수 같은 파형에서 얻음.
        # 즉 들어오는 X의 데이터는 사람이 있으면 1이상 없으면 0이게 되는 데
        # 각 데이터의 누적합을 통해서 sin cos인 마냥 파형을 이룬 데이터를 갖게 되고
        # 파형의 최대값 최소값 지점이 살균의 기준점이 되게 하는 방식
        '''
        사용한 변수
        길이 length
        dict로 통해 들어온 1. 시간 데이터 2. 사람 데이터

        살균시간이 결정되면 받을 변수인 data, 누적합을 통해 살균 척도를 정할 수 있도록 res
        '''
        length = len(x)
        data = []  # data를 받을 공간
        res = 0  # 누적합에 도움을 줄 변수!

        time_data = list(x.keys())  # 시간 데이터
        human_data = list(x.values())  # 사람 데이터

        before = human_data[0]

        for i in range(1, length):
            if human_data[i] == 0:  # 사람이 없을 때~
                if before == human_data[i]:  # 전과 비교 동일
                    res -= 1
                else:  # 전에 있다가 이제 없는 거 나름 살균 포인트
                    if res > 6:  # 나름 30분 넘게 있던거
                        print("up", time_data[i], i, res)
                        data.append(time_data[i])
                        res = 0
            else:  # 사람이 있을 때~
                if before == human_data[i]:  # 전과 비교 동일
                    res += 1
                else:
                    # 전에 없다가 이제 있는 거 나름 살균 포인트
                    print("dd", time_data[i - 1], i, res)
                    data.append(time_data[i - 1])
                    res = 0
            before = human_data[i]

        # 디버깅 용임 데이터가 없으면 그냥 살균시간 08시에 쏴줌
        if not data:
            data.append('08:00')

        return data

    # 살균알고리즘 기반 살균 시간 저장
    def save_cleantime(self):
        self.cleantime.clear()
        now = datetime.datetime.now()
        for i1,v  in enumerate(self.cleantime):
            id=self.STElist[i1]
            name=self.CAMlist[i1][1]
            for j in v:
                hour = int(j.split(':')[0])
                min = int(j.split(':')[1])
                date = datetime.datetime(now.year, now.month, now.day, hour, min, 0)
                str = date.strftime('%Y-%m-%d %H:%M:%S')
                cleanid=id+"="+str
                strength=""
                if self.cleanstrength[i1]==0: strength="하"
                elif self.cleanstrength[i1]==1: strength="중"
                else: strength="상"
                lock.acquire()
                self.cursor.execute('insert into cleandata values(%s,%s,%s,%s)',(id, name, str, "AI",cleanid,strength))
                self.db.commit()
                lock.release()

    def save_fivemin(self):
        now = datetime.datetime.now()  # 현재 날짜 얻어오기
        formatted_data = now.strftime('%Y-%m-%d')  # 현재 시간 문자열 포맷팅
        for i, v in self.CAMlist:
            fivemin_json = json.dumps(self.fiveMin_data_dict[i])
            lock.acquire()
            self.cursor.execute('insert into fivemindata values(%s,%s,%s)', (v, formatted_data, fivemin_json))
            self.db.commit()
            lock.release()

    def make_dict(self):
        for i, v in enumerate(self.CAMlist):
            temp=dict()
            myDatetime = datetime.datetime.strptime('00:00', '%H:%M')
            for j in range(288):
                formatted_data = myDatetime.strftime('%H:%M')  # 현재 시간 문자열 포맷팅
                temp[formatted_data]=self.fiveMin_data[i][j]
                myDatetime = myDatetime + datetime.timedelta(minutes=5)
            self.fiveMin_data_dict.append(temp)

    # 데이터 전처리(5분마다 처리)
    def make_fiveMin(self):
        fivedata=[]
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)

        sql_sel = "SELECT humann FROM humandata where id = %s and time between %s and %s"

        for i, name in enumerate(self.CAMlist):
            dStart = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
            dend = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
            while 1:
                next = dStart + datetime.timedelta(seconds=300)
                self.cursor.execute(sql_sel, (name, dStart, next))
                res = self.cursor.fetchall()
                list=[]
                for v in res:
                    list.append(v['cnt'])
                if list.count(0)>240:
                    fivedata.append(0)
                else:
                    sum=0
                    cnt=0
                    for i in list:
                        if i!=0:
                            sum+=i
                            cnt+=1
                    avg = sum/cnt
                    fivedata.append(avg)
                next_str = next.strftime('%Y-%m-%d %H:%M:%S')
                dStart = dStart + datetime.timedelta(seconds=300)
                if (dStart == dend):
                    next = dStart + datetime.timedelta(seconds=300)
                    self.cursor.execute(sql_sel, (name, dStart, next))
                    res = self.cursor.fetchall()
                    list = []
                    for v in res:
                        list.append(v['cnt'])
                    if list.count(0) > 240:
                        fivedata.append(0)
                    else:
                        sum = 0
                        cnt = 0
                        for i in list:
                            if i != 0:
                                sum += i
                                cnt += 1
                        avg = sum / cnt
                        fivedata.append(avg)
                    break
        self.fiveMin_data.append(fivedata)

    # 학습 데이터 검증
    def verificationData(self):
        now = datetime.datetime.now()
        now = now - datetime.timedelta(days=1)
        formatted_data = now.strftime('%Y-%m-%d')

        time1 = formatted_data + ' 00:00:00'
        time2 = formatted_data + ' 23:59:59'
        for name in self.CAMlist:
            # 특정 하루 기간 동안 저장된 데이터 개수 알아내기
            sql = "SELECT count(*) FROM test_table2 where id = %s and time between %s and %s"

            self.cursor.execute(sql, (name, time1, time2))
            res = self.cursor.fetchall()
            # 86400개 데이터가 아니라면 그날을 1초 단위로 반복하면서 데이터가 없다면 '0'으로 삽입
            if res[0]['count(*)'] != 86400:
                dStart = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
                dEnd = dStart + datetime.timedelta(days=1)
                while 1:
                    sql = "SELECT count(*) FROM test_table2 where id = %s and time = %s"
                    intime = dStart.strftime('%Y-%m-%d %H:%M:%S')
                    self.cursor.execute(sql, (name, intime))
                    res = self.cursor.fetchall()
                    if res[0]['count(*)'] == 0:
                        lock.acquire()
                        self.cursor.execute('insert into test_table2 values(%s,%s,%s)', (name, intime, '0'))
                        self.db.commit()
                        lock.release()
                    dStart = dStart + datetime.timedelta(seconds=1)
                    if dStart == dEnd:
                        break

    # 살균 명령 - AI
    def command_clean(self):
        while True:
            now = datetime.datetime.now()  # 현재 날짜 얻어오기
            formatted_data = now.strftime('%Y-%m-%d %H:%M')  # 현재 시간 문자열 포맷팅
            for i, v in enumerate(self.STElist):
                for j in self.cleantime[i]:
                    if formatted_data==j:
                        self.cid=self.STElist[i][0]
                        self.ccheck=True
                        self.cmd = "clean-"+str(self.cleanstrength[i])+"-"+self.STElist[i][0]+"="+formatted_data

    # 살균 명령 - 앱
    def command_clean_app(self, id):
        name=None
        for i, v in enumerate(self.STElist):
            if v==id:
                name=self.CAMlist[i][1]
                break
        now = datetime.datetime.now()  # 현재 날짜 얻어오기
        formatted_data = now.strftime('%Y-%m-%d %H:%M')  # 현재 시간 문자열 포맷팅
        cleanid = id+"="+formatted_data
        lock.acquire()
        self.cursor.execute('insert into cleandata values(%s,%s,%s,%s)', (id, name, formatted_data,"user",cleanid,"하"))  # 데이터 삽입
        self.db.commit()
        lock.release()

        self.cid = id
        self.ccheck = True
        self.cmd = "clean-0-"+cleanid

    # 카메라 라즈베리파이와 통신해서 데이터 삽입
    def cam_handler(self, conn, addr, name, terminator="bye"):
        pri_date=''
        while True:
            data = conn.recv(1024) # 데이터 받아옴
            if data == b"exit":
                break
            now = datetime.datetime.now() # 현재 날짜 얻어오기
            formatted_data = now.strftime('%Y=%m-%d %H:%M:%S') # 현재 시간 문자열 포맷팅
            if formatted_data==pri_date: # 이전에 저장한 시간 데이터와 같으면 패스
                continue
            pri_date=formatted_data
            print(name, formatted_data, data)
            lock.acquire()
            self.cursor.execute('insert into humandata values(%s,%s,%s)', (name, formatted_data, data)) # 데이터 삽입
            self.db.commit()
            lock.release()

    # 살규기 라즈베리파이와 통신해 여러 명령 전송 - 미완
    def clean_handler(self, conn, addr, name, terminator="bye"):
        while True:
            if self.cid==name and self.ccheck:
                self.cid = ''
                self.ccheck = False
                conn.send(self.cmd.encode(encoding='utf_8', errors='strict'))
                data = conn.recv(1024)
                if data== "clean":
                    pass
                else:
                    recv_data = data.split(',')
                    t = recv_data[0]
                    h = recv_data[1]
                    self.sensorValue.clear()
                    self.sensorValue.append(t)
                    self.sensorValue.append(h)
                    self.sensorCheck=True

    def run_server(self, host='', port=8888):
        check=False
        with socket.socket() as sock:
            sock.bind((host, port))
            while True:
                # 현재 시간과 인공지능 살균 시작 시간이 같으면 스케줄러  시작
                now = datetime.datetime.now()
                nowstrdate = now.strftime('%Y-%m-%d')
                if self.startDate==nowstrdate and check==False:
                    self.sched.start()
                    check=True
                # 소켓 스레드 통신
                sock.listen(5)
                conn, addr = sock.accept()
                id = conn.recv(1024).decode(encoding='utf_8', errors='strict')
                if id[0:3]=='CAM': # 통신대상이 카메라일 경우
                    temp = id.split(',')
                    id = temp[0]
                    name = temp[1]
                    temp_list = [id, name]
                    self.CAMlist.append(temp_list)
                    self.CAMlist.sort(key=lambda x: x[0][4])
                    t = Thread(target=self.cam_handler, name=id, args=(conn, addr, id))
                    t.start()
                elif id[0:3]=='STE': # 통신대상이 살균기일 경우
                    self.STElist.append(id)
                    self.STElist.sort(key=lambda x: x[4])
                    t = Thread(target=self.clean_handler, name=id, args=(conn, addr, id))
                    t.start()
            sock.close()
            self.sched.shutdown()
            self.cursor.close()
            self.db.close()
            print('server shutdown')


