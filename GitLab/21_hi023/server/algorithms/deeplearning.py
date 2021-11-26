#import tensorflow as tf
#from tensorflow.keras.layers import LSTM, Dense
import numpy as np
#from tensorflow.python.keras.layers.serialization import populate_deserializable_objects
from sklearn.cluster import KMeans
import json
from sqlalchemy import create_engine
import pandas as pd

# 실험용 데이터임! 간단히 작동은 되는 듯? !!!
# 살균의 상 중 하!
#physical_devices = tf.config.list_physical_devices('GPU')
#tf.config.experimental.set_memory_growth(physical_devices[0], True)


data_label =[2,1,1,0,0,2,0,2,1,2]

#주중 weekday 와 weekend를 구분하자가 프로젝트 핵심일 듯?







# 5min-data로 분류된 데이터가 들어오게 한다.
# 5-min은
# id<-varchar, time<-datetime, human <- json
def clustering_model(data):
    #군집의 개수는 사람이 정해줘야 한다!

    val = data['cam_id'].unique() #cam에 대한 unique데이터 추출
    cam_data ={}                  #cam의 숫자 만큼 데이터 생길 것임
    sterlizer={}
    #key == clustering 데이터 val : 실제 살균해줘야 하는 휴먼 데이터
    verification ={0:-1, 1:-1,2:-1} #-1로 초기화

    for name in val:
        cam_data[name]=[]
        sterlizer[name] = 0


    train_data =[]
    #일단 학습할 데이터들을 쭉 넣어
    for idx  in range(len(data)):
        pattern_data = data.iloc[idx]['human']  #json 이지만 실제로는 dict일 가능성 높
        cam_pos = data.iloc[idx]['cam_id']

        human_pattern = list(pattern_data.values())
        train_data.append(human_pattern) #2D array 학습데이터에다가도 쌓고
        cam_data[cam_pos].append(human_pattern) #나중에 분리할 곳에다가도 쌓고

    # train 2D array
    Kmean = KMeans(n_clusters=3)
    Kmean.fit(train_data)

    for cam, val in cam_data.items():
        # room의 휴먼의 사이즈를 보여줌
        human_size = label_func(val)

        tmp = np.array(Kmean.predict(val)).mean() #0, 1, 2의 값이 나올 것임
        if tmp < 1:
            tmp = 0
        elif 1<= tmp <1.6:
            tmp=1
        else:
            tmp=2

        verification[tmp] = human_size
        sterlizer[cam] =tmp


    for t_val in verification.keys():
        if sterlizer[cam] == t_val:
            sterlizer[cam] = verification[t_val]

    return sterlizer


#label을 위한 함수입니다.

# 사람이 얼마 정도 있는 지 예측해서 평균을 내어보는? 그런 느낌?
# in 2d array
def label_func(data):
    tmp =[]
    length=len(data)
    for i in range(length):
        label_data = np.delete(data[i],np.where(data[i] == 0)) #0을 제거~
        label_data = np.array(label_data).mean()
        tmp.append(label_data)

    tmp = np.array(tmp).mean()
    if tmp < 1.5 :
        return 0
    elif 1.5<= tmp and tmp <2.5:
        return 1
    else:
        return 2





import json


engine = create_engine('mysql+pymysql://root:@54.180.136.222/testdb',convert_unicode =True)
conn =engine.connect()

data = pd.read_sql_table('test_table2',conn)
print(data.head())
print("=================")
print(data['cnt'].unique(),len(data))
print("=================")
print(data.iloc[0]['id'])




# 테스트용 Python Dictionary
customer = '{"title": 1, "ISBN": 132, "author": "mk" }'

# JSON 인코딩
a = json.loads(customer)

a = [0,0,2,2,2,2,0,0,0,2]
b = [1,1,0,0,1,1,1,1,1,0]
c = [3,3,0,0,0,0,3,4,3,0]
t_data = [a,c,c,b,b,a,b,a,c,a]

#
Kmean = KMeans(n_clusters=3)
Kmean.fit(t_data)



print(Kmean.predict([a,b]))
# 문자열 출력
#print(a.keys(), a.values())
#print(type(a))  # class str