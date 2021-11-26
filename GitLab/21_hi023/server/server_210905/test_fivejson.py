import pymysql
import json
import datetime
import json
db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='1234',
                                  db='testdb',
                                  charset='utf8')
cursor = db.cursor(pymysql.cursors.DictCursor)

temp=dict()
myDatetime = datetime.datetime.strptime('00:00', '%H:%M')
for j in range(288):
    formatted_data = myDatetime.strftime('%H:%M')  # 현재 시간 문자열 포맷팅
    temp[formatted_data]=1
    myDatetime = myDatetime + datetime.timedelta(minutes=5)

temp = json.dumps(temp)

print(temp)

#cursor.execute('insert into fivemindata values(%s,%s,%s)',("CAM-0-0000", "2021-08-23", temp))
cursor.execute('insert into fivemindata values(%s,%s,%s)',("CAM-0-0000", "2021-08-24", temp))
cursor.execute('insert into fivemindata values(%s,%s,%s)',("CAM-0-0000", "2021-08-25", temp))

#cursor.execute('insert into fivemindata values(%s,%s,%s)',("CAM-1-1111", "2021-08-23", temp))
#cursor.execute('insert into fivemindata values(%s,%s,%s)',("CAM-1-1111", "2021-08-24", temp))
cursor.execute('insert into fivemindata values(%s,%s,%s)',("CAM-1-1111", "2021-08-25", temp))

#cursor.execute('insert into fivemindata values(%s,%s,%s)',("CAM-2-2222", "2021-08-23", temp))
cursor.execute('insert into fivemindata values(%s,%s,%s)',("CAM-2-2222", "2021-08-24", temp))
#cursor.execute('insert into fivemindata values(%s,%s,%s)',("CAM-2-2222", "2021-08-25", temp))
db.commit()


'''
def json_default(value):
    if isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d %H:%M:%S')

cursor.execute("SELECT human FROM fivemindata")
row = cursor.fetchone()
while row is not None:
    print(row)
    print(row['human'])
    row = cursor.fetchone()
'''
#data = json.dumps(cursor.fetchall(), default=json_default)
#cursor.execute("SELECT JSON_OBJECT('id', id, 'time', time, 'cnt', cnt) AS 'JSON Data' FROM test_table2")
