#!/usr/bin/env python
# coding: utf-8
#Ekin Celebi
#150160152

# In[1]:


import pandas
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import math 
colnames = ['Date','Open','High','Low','Close','Adj Close','Volume']
data = pandas.read_csv('AAPL.csv', names=colnames)
temp = data.Close
close = np.zeros(len(temp)-1)
for i in range(len(close)):
    close[i] = float(temp[i+1])
    


# In[2]:




new = np.zeros(len(close))

for x in range(len(close)):
    if x == 0:
        new[0] = close[0]/3
    elif x == 1:
        new[1] = (close[0] + close[1])/3
    else:
        new[x] = ((close[x]+close[x-1])+close[x-2])/3
        
        
##question 1
def convolve_signals(x_signal,h_signal):

    y_length = len(x_signal) + len(h_signal) - 1

    convolved = np.zeros(y_length)

    for i in range(y_length):
        k = i
        tmp = 0
        for j in range(len(h_signal)):
            if k>=0 and k<len(x_signal):
                tmp = tmp + (x_signal[k]*h_signal[j])
            
            k = k-1;
            convolved[i] = tmp;
        
    return convolved
        

print('x[n]=[0 1 2 3], h[n]=[1 1 1 1]')
print('Convolution: ', convolve_signals([0, 1, 2, 3], [1, 1, 1, 1]))


print('x[n]=[0 1 2 3], h[n]=[1]')
print('Convolution: ', convolve_signals([0, 1, 2, 3], [1]))


print('x[n]=[0 1 2 3], h[n]=[0 1 2 3]')
print('Convolution: ', convolve_signals([0, 1, 2, 3], [0, 1, 2, 3]))


print('x[n]=[1 0 1 2 3], h[n]=[1 2]')
print('Convolution: ', convolve_signals([1, 0, 1, 2, 3], [1, 2]))





def standardize(datas):
    temp_array =  [0] * 5
    return_array =  [0] * 400
    counter = 0
    counter2 = 0
    for frames in range(80):
        for index in range(5):
            temp_array[index] = datas[counter]
            counter = counter + 1
        
        mean_val = mean(temp_array)
        
        std_dev = np.std(temp_array)
        
        for index2 in range(5):
            return_array[counter2] = ( datas[counter2] - mean_val )/std_dev
            counter2 = counter2 + 1
        
        

    return return_array





plt.scatter(np.arange(400),standardize(close[-400:]), alpha=0.5)
plt.title('Standardization Demonstration')
plt.xlabel('Days')
plt.ylabel('Closing Price Values Standardized')
plt.show()




def normalize(datas):
    temp_array =  [0] * 5
    return_array =  [0] * 400
    counter = 0
    counter2 = 0
    for frames in range(80):
        for index in range(5):
            temp_array[index] = datas[counter]
            counter = counter + 1
        
        xmax = max(temp_array)
        
        xmin = min(temp_array)
        
        for index2 in range(5):
            return_array[counter2] = ( datas[counter2] - xmin )/(xmax-xmin)
            counter2 = counter2 + 1
        
        

    return return_array



plt.scatter(np.arange(400),normalize(close[-400:]), alpha=0.5)
plt.title('Normalization Demonstration')
plt.xlabel('Days')
plt.ylabel('Closing Price Values Normalized')
plt.show()









def max_convolution(datas,impulse):
    temp_array =  [0] * 5
    return_array =  [0] * 80
    counter = 0
    
    for frames in range(80):
        for index in range(5):
            temp_array[index] = datas[counter]
            counter = counter + 1
        
        
        
        return_array[frames] = max(convolve_signals(temp_array, impulse))
        

    return return_array






plt.scatter(np.arange(80),max_convolution(normalize(close[-400:]),[0.2, 0.4, 0.6, 0.8, 1]), alpha=0.5)

plt.title('h[n] = [0.2, 0.4, 0.6, 0.8, 1]')
plt.xlabel('Frames')
plt.ylabel('Maximum Convolution Values')
plt.show()






plt.scatter(np.arange(80),max_convolution(normalize(close[-400:]),[1, 0.5]), alpha=0.5)

plt.title('h[n] = [1, 0.5]')
plt.xlabel('Frames')
plt.ylabel('Maximum Convolution Values')
plt.show()


# In[47]:



plt.scatter(np.arange(80),max_convolution(normalize(close[-400:]),[0.5, 0.5, 0.5, 0.5, 0.5]), alpha=0.5)
plt.title('h[n] = [0.5, 0.5, 0.5, 0.5, 0.5]')
plt.xlabel('Frames')
plt.ylabel('Maximum Convolution Values')
plt.show()


# In[48]:



plt.scatter(np.arange(80),max_convolution(normalize(close[-400:]),[0.05, 0.1, 0.2, 0.4, 0.8]), alpha=0.5)
plt.title('h[n] = [0.05, 0.1, 0.2, 0.4, 0.8]')
plt.xlabel('Frames')
plt.ylabel('Maximum Convolution Values')
plt.show()







