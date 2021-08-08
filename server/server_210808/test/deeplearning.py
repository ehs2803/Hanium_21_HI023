import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os

data =[[0,1,1,0,0,0,1,0,0,0], [1,1,1,1,0,1,1,1,1,1]]

def make_model(x, y, a):
    model = tf.keras.Sequential()
    model.add(Dense(100, activation='relu', input_shape=(1,)))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dropout(rate=0.2))
    model.add(Dense(2, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    # #
    model.summary()
    model.fit(x, y, epochs=10, verbose=1, batch_size=1)
    #
    model_name = str(a)+'.h5'
    model.save(model_name)

def retrain_model(x, y, a):
    model_name = str(a) + '.h5'
    model = tf.keras.models.load_model(model_name)
    model.fit(x, y, epochs=10, verbose=1, batch_size=1)
    #
    model.save(model_name)


list = [['cam','a'],['dem','b']]

for i, v in enumerate(list):
    x=data[i]
    y=data[i]
    #x=np.array(x)
    #y=np.array(y)
    print(x)
    print(y)
    if not os.path.exists('model/'+v[0]+'/weekday'):
        os.makedirs('model/'+v[0]+'/weekday')
        make_model(x,y,'model/'+v[0]+'/weekday/weekday')
    else:
        retrain_model(x,y,'model/'+v[0]+'/weekday/weekday')


'''
cnt=0
for i in range(2):
    cnt+=1
    model_name = str(cnt)+'.h5'
    new_model = tf.keras.models.load_model('model/'+model_name)
    yhat = new_model.predict([0,1,2,3,4,5,6,7,8,9])
    print(yhat)

'''


