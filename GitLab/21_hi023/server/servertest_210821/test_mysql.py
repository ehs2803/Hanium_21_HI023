import pymysql

db = pymysql.connect(host='54.180.136.222',
                                  user='root',
                                  password='haniumhi_023',
                                  db='testdb',
                                  charset='utf8')
cursor = db.cursor(pymysql.cursors.DictCursor)

cursor.execute('select * from test_table2')

print(cursor.fetchall())