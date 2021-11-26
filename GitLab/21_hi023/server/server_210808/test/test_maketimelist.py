import datetime

now = datetime.datetime.now()
to = now+datetime.timedelta(days=1)

dStart = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
dend = datetime.datetime(now.year, now.month, now.day, 23, 55, 0)

timelist=[]
while 1:
    str = dStart.strftime('%Y-%m-%d %H:%M:%S')
    timelist.append(str)
    dStart = dStart + datetime.timedelta(seconds=300)
    if (dStart == dend):
        str = dStart.strftime('%Y-%m-%d %H:%M:%S')
        timelist.append(str)
        break

print(timelist)
print(len(timelist))

#20210801