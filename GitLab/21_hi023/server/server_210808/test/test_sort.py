#20210808

CAMlist =[['cam-0-0000', '거실'],['cam-2-2222', '거'],['cam-1-1111', '실'],['cam-6-6666', '방'],['cam-5-5555', '주방']]
CAMlist.sort(key=lambda x: x[0][4])

print(CAMlist)