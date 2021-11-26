import socket
import sys
import MySQLdb as mydb
from datetime import datetime

db = mydb.connect("localhost", "root", "server","testsql")
cur = db.cursor()

HOST = '' #all available interfaces
PORT = 8888

#1. open Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#2. bind to a address and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind Failed. Error code: ' + str(msg[0]) + ' Message: ' + msg[1])
    sys.exit()

print ('Socket bind complete')

#3. Listen for incoming connections
s.listen(10)
print ('Socket now listening')


#keep talking with the client
#4. Accept connection
conn, addr = s.accept()
print ('Connected with ' + addr[0] + ':' + str(addr[1]))
while 1:
    #5. Read/Send
    data = conn.recv(1024)
    if data=="exit":
        break
    #conn.sendall(data)
    datalist = data.split(',')
    x1=datalist[0]; y1=datalist[1]; x2=datalist[1]; y2=datalist[1]
    now=datetime.now()
    formatted_data = now.strftime('%Y=%m-%d %H:%M:%S')
    cur.execute('insert into test values(%s,%s,%s,%s,%s)', (formatted_data,x1,y1,x2,y2))
    conn.commit()
    print(data.decode())
    
    
conn.close()
s.close()
cur.close()
db.close()
