import math
import csv
from itertools import combinations
from math import gcd
import pandas as pd
import numpy as np
import decimal 

def gen():
    rv = []
    for i in range(0,365*4+1):
        rv.append(math.sin((math.pi/365)*i))

    print(len(rv))
    with open('data.csv', 'w') as myfile:
        wr = csv.writer(myfile, delimiter=',')
        wr.writerow(rv)


def process():
    rv = {}
    my_file = open("data.csv", 'r')
    reader = csv.reader(my_file, delimiter=',')
    data = list(reader)[0]
    baseline = data[0:366]

    for i in range(1,len(data)):
        test = data[i:365+i]
        error = 0
        for ind,val in enumerate(test):
            error += (float(val)-float(data[ind]))**2
        rv[i] = error
    
    sorted_d = sorted(rv.items(), key=lambda x: x[1])
    return sorted_d


def find_pattern2(l,ran):
    n = int(round(0.25*len(l)))
    sl = l[:n]
    dic = dict(sl)

    rv = {}
    for i in range(1,ran+1):
        for j,v in enumerate(dic):
            if v != 0:
                if v%i == 0:
                    rv[i] = rv.get(i,0) + 1
    s = pd.DataFrame(rv,index=[0]).transpose()
    s.to_csv('data4.csv')
    return s


def find_pattern3(l,ran):
    n = int(round(0.25*len(l)))
    sl = l[:n]
    rv = {}
    update = False
    for i in l:
        if i[0] != 0:
            for j in range(i[0]):
                if l[j][0]%i[0] == 0:
                    if l[j][0] != 0:
                        rv[j] = rv.get(j,0) + (1/l[j][0])**2
                        update = True
            if update == False:
                rv[i] = rv.get(i,0) + (1/(i[0]))**2

    s = pd.DataFrame(rv,index=[0]).transpose()
    s.to_csv('data5.csv')
    return s

def fourier1(l):
    l2 = []
    for v in l.values():
        l2.append((1/v)**2)
    print(l2)
    x = np.asarray(l2)

    w = np.fft.fft(x)
    freqs = np.fft.fftfreq(len(x))
    amps = np.abs(w)**2
    rv = {}

    print(type(amps))
    for freq,amps in zip(freqs, amps):
        period = 1/freq
        if period > 0:
            if period%1 == 0:
                rv[period] = amps
    sorted_d = sorted(rv.items(), key=lambda x: x[1])
    return sorted_d

def fourier2():
    l2 = []
    for i in range(300):
        if i%3 == 0:
            l2.append(10)
        else:
            l2.append(0.5)

    x = np.asarray(l2)
    w = np.fft.fft(x)
    freqs = np.fft.fftfreq(len(x))
    amps = np.abs(w)**2
    for freq,amps in zip(freqs, amps):
        if freq != 0:
            period = 1/freq
            if period > 0:
                if period%1 == 0:
                    print(period, amps)
