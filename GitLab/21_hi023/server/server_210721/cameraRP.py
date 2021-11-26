import socket
import sys
import pymysql
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time
from threading import Thread
import threading
lock = threading.Lock()

class Socket():
    def __init__(self):
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='1234',
                                  db='testdb',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def echo_handler(self, conn, addr, terminator="bye"):
        name = conn.recv(1024).decode(encoding='utf_8', errors='strict')
        while True:
            data = conn.recv(1024)
            if data == b"exit":
                break
            now = datetime.now()
            formatted_data = now.strftime('%Y=%m-%d %H:%M:%S')
            print(name, formatted_data, data)
            lock.acquire()
            self.cursor.execute('insert into test_table2 values(%s,%s,%s)', (name, formatted_data, data))
            self.db.commit()
            lock.release()

    def run_server(self, host='', port=8888):
        with socket.socket() as sock:
            sock.bind((host, port))
            while True:
                sock.listen(2)
                conn, addr = sock.accept()
                # 새 연결이 생성되면 새 스레드에서 에코잉을 처리하게 한다.
                t = Thread(target=self.echo_handler, args=(conn, addr))
                t.start()
            sock.close()

    def fininsh(self):
        self.scheduler.shutdown()
        self.s.close()
        self.conn.close()
        self.cursor.close()
        self.db.close()
        print('socket disconnect')

'''
class Socket():
    def __init__(self, port):
        self.scheduler = BackgroundScheduler()
        job = self.scheduler.add_job(self.job, 'interval', seconds=1)
        self.HOST=''
        self.PORT= port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ('Socket created')
        try:
            self.s.bind((self.HOST, self.PORT))
        except socket.error as msg:
            print('Bind Failed. Error code: ' + str(msg[0]) + ' Message: ' + msg[1])
            sys.exit()
        print('Socket bind complete')
        self.s.listen(10)
        print('Socket now listening')
        self.conn, self.addr = self.s.accept()
        print('Connected with ' + self.addr[0] + ':' + str(self.addr[1]))

        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='1234',
                                  db='testdb',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.name=self.conn.recv(1024).decode(encoding='utf_8', errors='strict')

    def startSC(self):
        self.scheduler.start()

    def job(self):
        self.readData()

    def readData(self):
        data = self.conn.recv(1024)
        if data==b"exit":
            self.fininsh()
            time.sleep(1)
        now = datetime.now()
        formatted_data = now.strftime('%Y=%m-%d %H:%M:%S')
        print(self.name, formatted_data, data)
        self.cursor.execute('insert into test_table2 values(%s,%s,%s)', (self.name, formatted_data, data))
        self.db.commit()
        #print(self.name, formatted_data,data)

    def fininsh(self):
        self.scheduler.shutdown()
        self.s.close()
        self.conn.close()
        self.cursor.close()
        self.db.close()
        print('socket disconnect')
        
'''