from multiprocessing import Pool,Queue
import os,time,random
from blinding_factor import Start
import datetime
import matplotlib.pyplot as plt


def pre_prepare(x):
    print('现在进入pre_prepare')
    print(x)
    for i in x:
        i[1]=i[1]+1
    return x

def prepare(x,master):
    print('现在进入prepare')
    for i in range(len(x)):
        A = x[0:i]
        B = x[i+1:]
        for t in A:
            t[1]=t[1]+1
        for t in B:
            t[1]=t[1]+1
    master[1]+=len(x)
    return x,master


def commit(x):
    print('现在进入commit')
    for i in range(len(x)):
        A = x[0:i]
        B = x[i+1:]
        for t in A:
            t[1]=t[1]+1
        for t in B:
            t[1]=t[1]+1
    return x


def PBFT(x):
    now = datetime.datetime.now()
    m = random.randint(0,len(x)-1)
    print('master 节点为:')
    master = x[m]
    print(master)
    del x[m]
    ##pre-prepare
    x = pre_prepare(x)
    print('pre_prepare阶段')
    print(x)
    ##prepare
    x,master= prepare(x,master)
    print('prepare阶段')
    print(x)
    ##commit
    x.append(master)
    x = commit(x)
    print(x)
    print('commit阶段')
    ##reply
    need_time = (datetime.datetime.now()-now).seconds
    return x,need_time+master[2]


def show_pic(x,y):
    plt.figure()
    plt.plot(x,y)
    plt.show()



def run(n):
    #q = Queue()
    p = Pool(n)
    #用于记录分组中的值
    results = []
    for i in range(n):
        # print('开始')
        results.append(p.apply_async(Start))
    # print('等待所有结束')
    p.close()
    p.join()
    # print('结束')
    temp = []
    for i in results:
        temp.append(i.get())

    y_time = [temp[0][1],temp[1][1]]
    x_number =[100,200]

    if len(temp)>2:
        for i in range(2,len(temp)):
            _,time=PBFT(temp[0:i])
            x_number.append((i+1)*200)
            y_time.append(time)
        show_pic(x_number,y_time)
    else:
        show_pic(x_number,y_time)


run(60)
   


