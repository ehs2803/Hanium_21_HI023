import datetime

startDate= datetime.datetime.now()
strtime = startDate.strftime('%Y=%m-%d')
print(strtime)

startDate = startDate + datetime.timedelta(days=1)
strtime = startDate.strftime('%Y=%m-%d')
print(strtime)