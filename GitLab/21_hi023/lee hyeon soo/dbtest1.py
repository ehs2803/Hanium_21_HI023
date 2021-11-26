import MySQLdb as mydb
db = mydb.connect("localhost", "root", "server","testsql")
cur = db.cursor()
cur.execute("select * from user")
while True:
	user = cur.fetchone()
	if not user:
		break
	print(user)
cur.close()
db.close()
