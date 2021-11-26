import datetime

#now = datetime.datetime.now()

myDatetime = datetime.datetime.strptime('00:00', '%H:%M')
list = []
'''
for i in range(288):
    formatted_data = myDatetime.strftime('%H:%M') # 현재 시간 문자열 포맷팅
    myDatetime = myDatetime + datetime.timedelta(minutes=5)
    print(formatted_data)
'''

temp=dict()
myDatetime = datetime.datetime.strptime('00:00', '%H:%M')
for j in range(288):
    formatted_data = myDatetime.strftime('%H:%M')  # 현재 시간 문자열 포맷팅
    temp[formatted_data]=1
    myDatetime = myDatetime + datetime.timedelta(minutes=5)
    list.append(temp)

print(list)