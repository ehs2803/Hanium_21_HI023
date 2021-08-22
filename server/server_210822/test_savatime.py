import datetime

timelist = ['18:30', '19:20', '20:00']

now = datetime.datetime.now()

for i in timelist:
    hour = int(i.split(':')[0])
    min = int(i.split(':')[1])
    date = datetime.datetime(now.year, now.month, now.day, hour, min, 0)
    str = date.strftime('%Y-%m-%d %H:%M:%S')
    print(str)