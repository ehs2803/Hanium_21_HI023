list1=[]

list1.append('CAM-2-4536')
list1.append('CAM-1-6812')
list1.append('CAM-3-2576')
list1.append('CAM-0-1234')

list1.sort(key= lambda x : x[4])
print(list1)

#20210731