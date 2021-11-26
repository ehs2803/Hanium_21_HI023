import tensorflow as tf
import time

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train, x_test = x_train / 255.0, x_test / 255.0


def x_and_y(num):

    # first
    if num==1:
        x_train_one = x_train[:15000]
        y_train_one = y_train[:15000]
        return x_train_one, y_train_one
        # first
    if num == 1:
        x_train_one = x_train[:15000]
        y_train_one = y_train[:15000]
        return x_train_one, y_train_one
        # first
    elif num == 2:
        # second
        x_train_two = x_train[15000:30000]
        y_train_two = y_train[15000:30000]
        return x_train_two, y_train_two
        # first
    elif num == 3:
        # third
        x_train_three = x_train[30000:45000]
        y_train_three = y_train[30000:45000]
        return x_train_three, y_train_three
    elif num == 4:
        # four
        x_train_four = x_train[45000:60000]
        y_train_four = y_train[45000:60000]
        return x_train_four, y_train_four




def create_model(x,y):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x, y, epochs=5)

    model.save('my_model_1.h5')

    model.evaluate(x_test, y_test, verbose=2)

def learning_model(x,y,num):
    string = 'my_model_{}.h5'.format(num-1)
    new_model = tf.keras.models.load_model(string)
    print("this is new model  "+str(num))
    new_model.evaluate(x, y)
    history = new_model.fit(x,y,epochs =5,shuffle =True)

    string = 'my_model_{}.h5'.format(num)
    new_model.save(string)
    new_model.evaluate(x_test, y_test, verbose=2)


a = int(input("입력 초기 값"))

tm = time.localtime(time.time())
#time_struct타입을 반환해줌 이거 기반으로 충분히 다음 날 되면 학습 시키기 가능할 것 같은 데?
while True:
    print(time.ctime(time.time()))
    x, y = x_and_y(a)
    if a == 1 :
        create_model(x, y)
    else:
        learning_model(x, y, a)
    a=a+1
    if a== 5:
        break
