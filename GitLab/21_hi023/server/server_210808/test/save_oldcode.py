def make_fiveMin(self):
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)

    sql_sel = "SELECT cnt FROM test_table2 where id = %s and time between %s and %s"
    sql_in = "insert into five_table values(%s,%s,%s)"

    for name in self.CAMlist:
        dStart = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
        dend = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        while 1:
            next = dStart + datetime.timedelta(seconds=300)
            self.cursor.execute(sql_sel, (name, dStart, next))
            res = self.cursor.fetchall()
            data0 = 0
            data1 = 1
            for v in res:
                if v['cnt'] == 1:
                    data1 += 1
                else:
                    data0 += 0
            data = 0
            if data1 / (data1 + data0) >= 80:
                data = 1
            else:
                data = 0
            next_str = next.strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute(sql_in, (name, next_str, data))
            dStart = dStart + datetime.timedelta(seconds=300)
            if (dStart == dend):
                next = dStart + datetime.timedelta(seconds=300)
                self.cursor.execute(sql_sel, (name, dStart, next))
                res = self.cursor.fetchall()
                data0 = 0
                data1 = 1
                for v in res:
                    if v['cnt'] == 1:
                        data1 += 1
                    else:
                        data0 += 0
                data = 0
                if data1 / (data1 + data0) >= 80:
                    data = 1
                else:
                    data = 0
                next_str = next.strftime('%Y-%m-%d %H:%M:%S')
                self.cursor.execute(sql_in, (name, next_str, data))
                break

#20210801