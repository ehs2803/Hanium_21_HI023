import pymysql
import datetime
import time
import threading
lock = threading.Lock()

starttime = time.time()

db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='1234',
                                  db='testdb',
                                  charset='utf8')

cursor = db.cursor(pymysql.cursors.DictCursor)

now = datetime.datetime.now()
formatted_data = now.strftime('%Y-%m-%d')

time1 = formatted_data+' 00:00:00'
time2 = formatted_data+' 23:59:59'

sql = "SELECT count(*) FROM test_table2 where id = %s and time between %s and %s"

name="CAM1111"
cursor.execute(sql, (name, time1, time2))
res = cursor.fetchall()

if res[0]['count(*)']!=86401:
    dStart = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    dEnd = dStart + datetime.timedelta(days=1)
    print(dStart, dEnd)
    cnt=0
    while 1:
        sql = "SELECT count(*) FROM test_table2 where id = %s and time = %s"
        intime = dStart.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql, (name, intime))
        res = cursor.fetchall()
        if res[0]['count(*)']==0:
            cnt+=1
            lock.acquire()
            cursor.execute('insert into test_table2 values(%s,%s,%s)', (name, intime, '0'))
            db.commit()
            print(name,intime)
            lock.release()
        dStart = dStart + datetime.timedelta(seconds=1)
        if dStart == dEnd:
            break
    print(cnt)

cursor.close()
db.close()
print(time.time()-starttime)
# db에서 select해서 정보 합차기

'''
now = datetime.datetime.now()
formatted_data = now.strftime('%Y-%m-%d')

time1 = formatted_data+' 00:00:00'
time2 = formatted_data+' 23:59:59'

sql = "SELECT count(*) FROM test_table2 where id = %s and time between %s and %s"

cursor.execute(sql, ("CAM1111", time1, time2))
res = cursor.fetchall()

#####################################################################


ans=0
d = datetime.datetime(2018, 5, 19,0,0,0)

while 1:
    ans += 1
    d = d+datetime.timedelta(seconds=1)
    if d ==datetime.datetime(2018, 5, 20,0,0,0):
        break
print(ans)
'''


'''
sql = "SELECT * FROM test_table2 where id = %s and cnt = %s"

cursor.execute(sql, ("CAM1111", '1'))
res = cursor.fetchall()

for data in res:
        print(data)

'''