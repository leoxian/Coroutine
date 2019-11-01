from multiprocessing import Pool
import time,random

def long_time_task(name):
    for i in range(0,10):
        print('hello_{}'.format(name))
        time.sleep(random.randint(0,1))


P = Pool()
temp_list=['leo','vicky','jack','jody']
for i in temp_list:
    P.apply_async(long_time_task,args=(i,))
P.close()
P.join()