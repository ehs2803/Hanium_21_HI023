import datetime

now = datetime.datetime.now() # 현재 날짜 얻어오기
formatted_data = now.strftime('%Y-%m-%d %H:%M') # 현재 시간 문자열 포맷팅

date = datetime.datetime.strptime(formatted_data,'%Y-%m-%d %H:%M')
print(date)
print(type(date))
print(date.year)
print(date.month)
print(date.day)
print(date.hour)
print(date.minute)