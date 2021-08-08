testlist=[]

a=[1,2,3]

for i in range(a):
    testlist.append([])

for i, v in enumerate(a):
    testlist[i].append(v)

data=0
if len(a)==0:
    data=1

#20210801