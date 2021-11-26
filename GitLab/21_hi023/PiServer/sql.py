import pymysql
 
# database에 접근
db= pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='1234',
                     db='testdb',
                     charset='utf8')
 
# database를 사용하기 위한 cursor를 세팅합니다.
cursor= db.cursor()

