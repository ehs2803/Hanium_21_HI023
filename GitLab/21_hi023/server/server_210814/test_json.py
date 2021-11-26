import pymysql
import json
import datetime

db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='1234',
                                  db='testdb',
                                  charset='utf8')
cursor = db.cursor(pymysql.cursors.DictCursor)

def json_default(value):
    if isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d %H:%M:%S')


cursor.execute("SELECT * FROM test_table2 where id='NO20210721' order by time desc")
data = json.dumps(cursor.fetchall(), default=json_default)
print(data)
print(type(data))


#cursor.execute("SELECT JSON_OBJECT('id', id, 'time', time, 'cnt', cnt) AS 'JSON Data' FROM test_table2")
print(type([{"id": "NO20210721", "time": "2021-07-21 17:34:45", "cnt": 0}]))