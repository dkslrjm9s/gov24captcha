import os
import cv2
import numpy as np
import tensorflow as tf
x_trainDir = "img"
y_trainDir = "label"
modelName = "captchaC"

startx = 10
length = 130
width = 18
captchaWidth = 18
arrange = 2


rang = range(-arrange, arrange)

len_train = len(os.listdir(y_trainDir)) * len(rang) * 6
x_train = np.zeros((len_train, 50, captchaWidth), dtype=np.float)
y_train = np.zeros((len_train, 1), dtype=np.int)
result = []

f = os.listdir(x_trainDir)

for i in range(len(os.listdir(x_trainDir))):
    img = cv2.imread(x_trainDir + "/" + f[i], cv2.IMREAD_GRAYSCALE)
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_not(img)  # 반전

    label = open(y_trainDir + "/" + f[i].split(".")[0] + ".csv", "r")
    lb = list(map(int, label.read().split(",")))
    label.close()

    for j in range(len(lb)):
        for k in range(len(rang)):
            x_train[i * 6 + j * len(rang) + k] = img[:, lb[j] + rang[k]:lb[j] + rang[k] + width] / 255.
            y_train[i * 6 + j * len(rang) + k] = int(f[i].split(".")[0][j])

if len(x_train) != len(y_train):
    print("갯수가 맞지 않습니다.")
    exit()

# create model
# x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(50, width)),
    tf.keras.layers.Dense(200, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax")
])

model.compile(loss='sparse_categorical_crossentropy', optimizer="rmsprop", metrics=['accuracy'])
# train model
model.fit(x_train, y_train, epochs=200, verbose=1)

model.save(modelName)
np.set_printoptions(formatter={'float_kind': lambda x: "{0:0.3f}".format(x)})
# print(y_train)
rs = list(y_train)
pd = list(model.predict(x_train))

print(1)

