from gevent import monkey;monkey.patch_all()
import gevent
import random
import datetime
import matplotlib.pyplot as plt

x = []
y = []
temp_x=[]
# group_list=[201,401,601,801,1001,1201,1401,1601,1801,2001,2201,2401,2601,2801,3001]
# group_list=[201,401,601,801,1001,1301,1501]
group_list=[101,201,301,401,501,601,701,801,901,1001,1101,1201,1301,1401,1501,1601,1701,1801,1901,2001,2101,2201,2301,2401,2501,2601,2701,2801,
            2901,3001,3101,3201,3301,3401,3501,3601,3701,3801,3901,4101,4201,4301,4401,4501,4601,4701,4801,4901,5001,5101,5201,5301,5401,5501,
            5601,5701,5801,5901,6001,6101,6201,6301,6401,6501,6601,6701,6801,6901,7001]
divide_list=[0]

def pre_prepare(x):
    print('现在进入pre_prepare')
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
    print('commit阶段')
    print(x)
    ##reply
    return x


 
def pow_goroutine(Id,difficult,sleep_time):
    n = 1
    start_time = datetime.datetime.now()
    #while n<10:
    while n<1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:
        #.strftime('%H:%M:%S.%f'
        #now_time = datetime.datetime.now()
        #print('开始进行计算:id:{}'.format(Id))
        n = random.randint(1,10)*n
        #gevent.sleep(sleep_time)
        gevent.sleep(1)
        #if Id>301:
        #print('这是新的')
        print('n:{},id:{}'.format(n,Id))
    #print('n:{},id:{},time:{}'.format(n,Id,datetime.datetime.now().strftime('%H:%M:%S.%f')))
    time_stamp=(datetime.datetime.now()-start_time).total_seconds()
    return (Id,n,time_stamp)
    
    #gevent.killall(temp)

for group in group_list:
    now_time = datetime.datetime.now()
    temp=[]
    for Id in range(0,group):
        difficult = random.randint(0,1000000000000)
        sleep_time = random.randint(0,2)
        temp.append(gevent.spawn(pow_goroutine,Id,difficult,sleep_time))

    gevent.joinall(temp)

    print('从这里开始')
    sort_temp=[]
    for _,g in enumerate(temp):
        print(g.value)
        sort_temp.append(g.value)

    h = 0
    sort_temp_result=[]
    divide_list.append(group-1)
    for s in divide_list:
        A =sort_temp[h:s]
        h = s
        sort_temp_result.append(A)
    sort_final=[]
    print('开始排序并且输出')
    for i in sort_temp_result:
        if len(i)!=0: 
            i=sorted(i,key=lambda k:k[2])
            sort_final.append(i[0])
            temp_x.append([i[0][0],0])
            print(i[0])
        else:
            pass
    print(len(temp_x))

    print('PoW 阶段总时间')
    print((datetime.datetime.now()-now_time).seconds)

    
    if len(temp_x)>2:
        print('从这里开始进入PBFT')
        temp_x=PBFT(temp_x)
    print((datetime.datetime.now()-now_time).seconds)
    y.append((datetime.datetime.now()-now_time).seconds)
    temp_x=[]
##
x =[]

for i in group_list:
    x.append(i-1)

plt.figure()
plt.plot(x,y)
plt.show()

