f = open("train.txt", 'w')
for i in range(1, 301):
    data = "data/img/aloe_"+'%03d'%(i)+'.jpg\n'
    f.write(data)
f.close()

