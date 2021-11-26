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
        self.CAMlist=[]
        self.STElist=[]

    def cam_handler(self, conn, addr, name, terminator="bye"):
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

    def clean_handler(self, conn, addr, name, terminator="bye"):
        while True:
            print(name)
            time.sleep(1)
            data = conn.recv(1024)
            if data == b"exit":
                break
            elif data[0:12]=="cleanResult":
                pass

            now = datetime.now()
            formatted_data = now.strftime('%Y=%m-%d %H:%M:%S')
            print(name, formatted_data, data)


    def run_server(self, host='', port=8888):
        with socket.socket() as sock:
            sock.bind((host, port))
            while True:
                sock.listen(5)
                conn, addr = sock.accept()
                name = conn.recv(1024).decode(encoding='utf_8', errors='strict')
                if name[0:3]=='CAM':
                    self.CAMlist.append(name)
                    t = Thread(target=self.cam_handler, name=name, args=(conn, addr, name))
                    t.start()
                elif name[0:3]=='STE':
                    self.STElist.append(name)
                    t = Thread(target=self.clean_handler, name=name, args=(conn, addr, name))
                    t.start()
            sock.close()

    def fininsh(self):
        #self.scheduler.shutdown()
        #self.conn.close()
        self.cursor.close()
        self.db.close()
        print('socket disconnect')

