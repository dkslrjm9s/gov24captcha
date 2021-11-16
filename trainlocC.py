import os

import cv2
import numpy as np
import tensorflow as tf

x_trainDir = "img"
y_trainDir = "label"
modelName = "locationC"

startx = 10
length = 130
width = 18

len_train = len(os.listdir(y_trainDir)) * length
x_train = np.zeros((len_train, 50, width), dtype=np.float)
y_train = np.zeros((len_train, 2), dtype=np.int)
result = []

f = os.listdir(x_trainDir)
for i in range(len(os.listdir(x_trainDir))):
    img = cv2.imread(x_trainDir + "/" + f[i], cv2.IMREAD_GRAYSCALE)
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_not(img) # 반전

    label = open(y_trainDir + "/" + f[i].split(".")[0] + ".csv", "r")
    lb = list(map(int, label.read().split(",")))
    label.close()

    for j in range(length):
        x_train[i * length + j] = img[:, startx + j:startx + j + width] / 255.

        lbl = []
        rg = range(startx + j, startx + j + width)
        chk = False
        for k in range(len(lb)):
            if lb[k] in rg:
                lbl.append(rg.index(lb[k]))
                chk = True
                break
        if chk:
            try:
                if lb[k + 1] in rg:
                    lbl.append(rg.index(lb[k + 1]))
                else:
                    lbl.append(width + width//2)
            except:
                lbl.append(width + width//2)
        else:
            lbl.append(-width//2)
            lbl.append(width + width//2)

        y_train[i * length + j, 0] = lbl[0]
        y_train[i * length + j, 1] = lbl[1]

if len(x_train) != len(y_train):
    print("갯수가 맞지 않습니다.")
    exit()

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(50, width)),
    tf.keras.layers.Dense(1300, activation="relu"),
    tf.keras.layers.Dense(200, activation="relu"),
    tf.keras.layers.Dense(2)
])

model.compile(loss='mse', optimizer="rmsprop", metrics=['accuracy'])
model.fit(x_train, y_train, epochs=200, verbose=1) # train model
np.set_printoptions(formatter={'float_kind': lambda x: "{0:0.3f}".format(x)})

model.save(modelName)


rs = list(y_train)
pd = list(model.predict(x_train))
total = 0
cor = 0
for i in range(len(rs)):
    num = np.array(list(map(int, rs[i])) - np.array(list(map(int, pd[i]))))
    if num[0] == 0 and num[1] == 0:
        continue
    if rs[i][0] < 0 and pd[i][0] < 0 and rs[i][1] > width and pd[i][1] > width:
        continue

    num = np.abs(num)
    if num[0] < 2 and num[1] < 2:
        cor += 1
    else:
        print("정답", list(map(int, rs[i])))
        print("예측", list(map(int, pd[i])))
        print("차이", num)
        print("================================")
    total += 1



print("정확도", float(cor)/total)
print("전체", total)
print("정답", cor)

