'''
print(1<<1)
print(1<<2)
print(1<<3)
print(1<<4)
print(1<<5)
'''

datas=[[1,0,0,1],[0,0,1,1]]
data=[]
for i in range(len(datas[0])):
    temp=''
    for j in range(len(datas)):
        temp= str(datas[j][i]) + temp
    temp = int(temp,2)
    data.append(temp)
for i in data:
    print(i)
#############################################
command_data=[]
for i in range(len(datas)):
    command_data.append([])

for i in data:
    b="{0:b}".format(i).zfill(len(datas)) #str(bin(i))[2:]
    for j in range(len(datas)):
        command_data[j].append(int(b[len(b)-j-1]))

print(command_data)

#20210731