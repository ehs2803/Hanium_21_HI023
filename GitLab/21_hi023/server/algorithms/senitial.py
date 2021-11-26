import pandas as pd

a= pd.read_csv('mon_sample.csv')





# 알고리즘에는 dict 형태로 들어온다고 생각
# 



def algorithms(x):
    #살균 알고리즘의 아이디어는 sin, cos함수 같은 파형에서 얻음.
    # 즉 들어오는 X의 데이터는 사람이 있으면 1이상 없으면 0이게 되는 데
    # 각 데이터의 누적합을 통해서 sin cos인 마냥 파형을 이룬 데이터를 갖게 되고
    # 파형의 최대값 최소값 지점이 살균의 기준점이 되게 하는 방식?

    ''' 
    사용한 변수 
    길이 length
    dict로 통해 들어온 1. 시간 데이터 2. 사람 데이터

    살균시간이 결정되면 받을 변수인 data, 누적합을 통해 살균 척도를 정할 수 있도록 res
    '''

    length = len(x)
    data = []   #data를 받을 공간
    res =0      #누적합에 도움을 줄 변수!

    time_data  = list(x.keys()) #시간 데이터
    human_data = list(x.values()) #사람 데이터


    before =human_data[0]
    
    for i in range(1,length):
        if human_data[i] == 0:           #사람이 없을 때~
            if before ==human_data[i]:    #전과 비교 동일
                res -=1
            else:                #전에 있다가 이제 없는 거 나름 살균 포인트
                if res > 6:      # 나름 30분 넘게 있던거
                    print("up",time_data[i], i, res)
                    data.append(time_data[i])
                    res = 0
        else:                   #사람이 있을 때~
            if before ==human_data[i]:    #전과 비교 동일
                res +=1
            else:
                            #전에 없다가 이제 있는 거 나름 살균 포인트
                print("dd",time_data[i-1], i, res)
                data.append(time_data[i-1])
                res=0
        before = human_data[i]
    
    #디버깅 용임 데이터가 없으면 그냥 살균시간 08시에 쏴줌
    if not data :
        data.append('08:00')
        pass

    return data

p=dict(zip(a['time'],a['human'])) #ok
res = algorithms(p)
print(res)