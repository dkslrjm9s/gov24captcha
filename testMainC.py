import os
import numpy as np
import cv2
import tensorflow as tf
import time
from sklearn.cluster import KMeans
from statistics import mean

startx = 10
length = 130
stride = 15
width = 18
captchaWidth = 18
locmodel = tf.keras.models.load_model("locationC")
capmodel = tf.keras.models.load_model("captchaC")


x_trainDir = "testimg"

total = 0
err = 0
avrTime = 0
for file in os.listdir(x_trainDir):
    if ".png" not in file:
        continue
    start = time.time()
    img = cv2.imread(x_trainDir + "/" + file, cv2.IMREAD_GRAYSCALE)
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    # 반전
    img = cv2.bitwise_not(img) / 255.0

    # f = open("label" + "/" + file.split(".")[0] + ".csv", "r")
    # testlb = list(map(int, f.read().split(",")))
    # f.close()

    x_test = np.zeros((int(length/stride) + 1 , 50, width), dtype=np.float)
    x_testind = 0
    for j in range(0,length,stride):
        x_test[x_testind] = img[:, startx + j:startx + j + width]
        x_testind += 1

    pd = list(locmodel.predict(x_test))
    ls = []
    for p in range(len(pd)):
        if int(pd[p][0]) > -1 and int(pd[p][0]) < width:
            ls.append(startx + (p * stride) + int(pd[p][0]))
        if int(pd[p][1]) > -1 and int(pd[p][1]) < width:
            ls.append(startx + (p * stride)+ int(pd[p][1]))


    # print(ls)
    kmodel = KMeans(6)
    kmodel.fit(np.array(ls).reshape(len(ls), 1))
    labels = kmodel.labels_
    # print(labels)
    ls_index = []
    for i in range(6):
        ls_index.append(int(mean([ls[i] for i in np.where(labels == i)[0].tolist()])))
    ls_index.sort()
    # print(ls_index)



    #숫자확인
    x_test = np.zeros((6, 50, captchaWidth), dtype=np.float)

    for j in range(6):
        x_test[j] = img[:, ls_index[j] : ls_index[j] + captchaWidth]
    pd = list(capmodel.predict(x_test))
    # print([np.argmax(i) for i in captcha2.predict(x_test)])
    result = "".join(list(map(str, [np.argmax(i) for i in capmodel.predict(x_test)])))
    avrTime += time.time() - start

    total += 1
    print(file, ":", result, "time : ", time.time() - start, end="")
    if result != file[:6]:
        err += 1
        print("    틀림")
        print(ls_index)
    else:
        print("")

print(100.0 * (total-err)/total)
print(avrTime/total)