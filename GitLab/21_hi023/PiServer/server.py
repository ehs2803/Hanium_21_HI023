from socket import *

print("1")
serverSock = socket(AF_INET, SOCK_STREAM)
print("2")
serverSock.bind(('', 8080))
print("3")
serverSock.listen(1)
print("4")
connectionSock, addr = serverSock.accept()
print("5")
print(str(addr),'에서 접속이 확인되었습니다.')

data = connectionSock.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))

connectionSock.send('I am a server.'.encode('utf-8'))
print('메시지를 보냈습니다.')

