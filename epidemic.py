import math
import matplotlib.pyplot as plt

def show_pic(x,y):
    plt.figure()
    plt.plot(x,y)
    plt.show()


y_temp = []
x_temp = []
for i in range(20,10000):
    y_temp.append(math.log(i,4))
    x_temp.append(i)

show_pic(x_temp,y_temp)