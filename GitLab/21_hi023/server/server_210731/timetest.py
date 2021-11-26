import datetime

now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=1)


dStart = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
dend = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 55, 0)

cnt=0
while 1:
    cnt+=1
    next = dStart + datetime.timedelta(seconds=300)
    print(dStart,next)
    dStart = dStart + datetime.timedelta(seconds=300)
    if (dStart == dend):
        next = dStart + datetime.timedelta(seconds=300)
        print(dStart, next)
        break


print(cnt)

#20210731