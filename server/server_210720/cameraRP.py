import socket
import sys
import pymysql
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

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
        self.cursor.execute('insert into test_table values(%s,%s)', (formatted_data, data))
        self.db.commit()
        print(formatted_data,data)

    def fininsh(self):
        self.scheduler.shutdown()
        self.s.close()
        self.conn.close()
        self.cursor.close()
        self.db.close()
        print('socket disconnect')
