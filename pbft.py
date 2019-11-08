import matplotlib.pyplot as plt
import random


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
    import time
    now = time.time()
    #print(now)
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
    need_time = time.time()-now
    #print(need_time)
    return x,round(need_time*1000,3)

  

def show_pic(x,y):
    plt.figure()
    plt.plot(x,y)
    plt.show()


temp =[]
for i in range(0,10000):
    temp.append([i,0])

y_time =[]
x_number =[]
for i in range(2,2000):
    _,time = PBFT(temp[0:i])
    #print(time)
    x_number.append(i+1)
    y_time.append(time)
show_pic(x_number,y_time)
