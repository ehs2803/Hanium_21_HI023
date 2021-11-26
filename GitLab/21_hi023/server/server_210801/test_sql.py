import pymysql
import datetime
import time
import threading
lock = threading.Lock()



db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='1234',
                                  db='testdb',
                                  charset='utf8')

cursor = db.cursor(pymysql.cursors.DictCursor)


sql = "SELECT cnt FROM test_table2 where id = %s and time between %s and %s"
time1='2021-07-23 13:49:28'
time2='2021-07-23 13:49:40'
name="CAM111"
cursor.execute(sql, (name, time1,time2))
res = cursor.fetchall()
for i in res:
    print(i['cnt'])


cursor.close()
db.close()

#20210731
