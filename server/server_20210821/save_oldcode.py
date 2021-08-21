def save_fivemin(self):
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    for i, v in self.CAMlist:
        id = v[0]
        time = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
        for j in self.fiveMin_data[i]:
            lock.acquire()
            self.cursor.execute('insert into test_table4 values(%s,%s,%s)', (id, time, str(j)))
            self.db.commit()
            lock.release()
            time = time + datetime.timedelta(seconds=300)