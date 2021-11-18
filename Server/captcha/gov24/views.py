from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import AnaResults
from .serializers import AnaResultsSerializer

from uuid import uuid4

import urllib.request
from io import BytesIO
import random
from PIL import Image
import urllib.request
import numpy as np
import cv2
import tensorflow as tf
import time
from sklearn.cluster import KMeans
from statistics import mean
import os
startx = 10
length = 130
width = 18
captchaWidth = 18
locmodel = tf.keras.models.load_model("locationC")
capmodel = tf.keras.models.load_model("captchaC")
kmodel = KMeans(6)
# Create your views here.


@csrf_exempt
def Main(request):
    return render(request, 'gov24/main.html')

@csrf_exempt
def AnalysisResult(request):
    if request.method == 'GET':

        if os.path.isfile("./gov24/curImg/img.png") :
            os.remove("./gov24/curImg/img.png")


        x_test = np.zeros((length, 50, width), dtype=np.float)
        ls = []
        ls_index = []

        captcha = urllib.request.urlopen("https://www.gov.kr/nlogin/captcha?id=" + str(random.random()))

        img = Image.open(BytesIO(captcha.read()))
        img = img.convert("L")

        img = np.array(img)
        noprocess = img
        cv2.imwrite("./gov24/curImg/img.png", noprocess)

        start = time.time()
        ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
        # 반전
        img = cv2.bitwise_not(img) / 255.0

        for j in range(length):
            x_test[j] = img[:, startx + j:startx + j + width]

        pd = list(locmodel.predict(x_test))

        for p in range(len(pd)):
            if int(pd[p][0]) > -1 and int(pd[p][0]) < width:
                ls.append(startx + p + int(pd[p][0]))
            if int(pd[p][1]) > -1 and int(pd[p][1]) < width:
                ls.append(startx + p + int(pd[p][1]))

        # print(ls)

        kmodel.fit(np.array(ls).reshape(len(ls), 1))

        labels = kmodel.labels_
        # print(labels)
        for i in range(6):
            ls_index.append(int(mean([ls[i] for i in np.where(labels == i)[0].tolist()])))
        ls_index.sort()
        # print(ls_index)

        # 숫자확인
        x_test = np.zeros((6, 50, captchaWidth), dtype=np.float)

        for j in range(6):
            x_test[j] = img[:, ls_index[j]: ls_index[j] + captchaWidth]

        result = "".join(list(map(str, [np.argmax(i) for i in capmodel.predict(x_test)])))
        totaltime = time.time() - start
        uuid = str(uuid4().hex)
        imgpath = "./gov24/static/data/" + uuid + "_" + result + ".png"
        htmlpath = uuid + "_" + result + ".png"
        cv2.imwrite(imgpath, noprocess)

        return render(request, 'gov24/main.html', {'result':result , 'time':str(totaltime), 'imgname':htmlpath})