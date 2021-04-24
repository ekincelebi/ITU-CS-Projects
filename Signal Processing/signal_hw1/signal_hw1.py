#!/usr/bin/env python
# coding: utf-8

#Ekin Celebi
#150160152
# In[116]:


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
    







new = np.zeros(len(close))

for x in range(len(close)):
    if x == 0:
        new[0] = close[0]/3
    elif x == 1:
        new[1] = (close[0] + close[1])/3
    else:
        new[x] = ((close[x]+close[x-1])+close[x-2])/3
        





plt.plot(close)
plt.ylabel('Closing Price Value')
plt.show()




plt.plot(new)
plt.ylabel('Moving average filter')
plt.show()






avg = mean(new)
print("The average is ", avg)





stand_dev = np.std(new)
print("Standard deviation is ", stand_dev)






def rms(arr, n): 
   square = 0
   mean = 0.0
   root = 0.0
     
   
   for i in range(0,n): 
       square += (arr[i]**2) 
   
   mean = (square / (float)(n)) 
     
    
   root = math.sqrt(mean) 
     
   return root





print("Root mean square" ,rms(new, len(new)))

