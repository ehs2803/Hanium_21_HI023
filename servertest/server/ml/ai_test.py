import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
#sched = BlockingScheduler()


df = pd.read_csv("mon_sample.csv")
#df = df.set_index('time')


val=np.array(df.index)

re_x = np.array(df['human'].values)
re_x=np.array(re_x).reshape(re_x.shape[0],1)

print(re_x.shape)

re_y =np.array(df['human'].values)

print(re_y.shape)



#@sched.scheduled_job('interval', minutes=1)
def make_model():
    model = tf.keras.Sequential()
    model.add(Dense(100, activation='relu', input_shape=(1,)))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dropout(rate=0.2))
    model.add(Dense(2, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    # #
    model.summary()
    model.fit(re_x, re_y, epochs=10, verbose=1, batch_size=1)
    #
    model.save('ai.h5')




make_model()

num=276
test_x = val[:num]
real_y = re_y[:num]


new_model = tf.keras.models.load_model('ai.h5')
yhat = new_model.predict(re_x[:num])


print(yhat)
print(yhat.shape)
print(tf.argmax(yhat,axis=1))
tmp = np.array(tf.argmax(yhat,axis=1))


print(tmp)

print(re_y)
print(tmp.shape, re_y.shape)
print((tmp == re_y))
# yhat= yhat.reshape(num,1)
# 
# plt.plot(test_x, real_y,'or')
# #plt.plot(test_x,yhat,'ob')
# plt.show()
#sched.start()