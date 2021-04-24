#!/usr/bin/env python
###Ekin Çelebi
###150160152
# coding: utf-8

# In[34]:


import pandas
import numpy as np
import math
import matplotlib.pyplot as plt
import librosa as librosa
from scipy.fft import fft, ifft

samples, rate = librosa.load('Africa.wav',sr=None,mono=True,offset =0.0,duration=None)


# In[35]:


from IPython.display import Audio
Audio('Africa.wav')


# In[36]:


from librosa import display
plt.figure()

librosa.display.waveplot(y=samples,sr=rate)
plt.xlabel('time in seconds')
plt.ylabel('Amplitude')
plt.show()


# In[37]:


def complexMean(arr):
    #returns mean of complex numbers
    n = len(arr)
    s = np.sum(arr)
    mean = np.real(s) / n + 1j * np.imag(s) / n
    return mean


# In[38]:


def radix2(inarray,N,outarray,twid):
    '''
    inarray: audio samples
    N:number of radix points
    outarray:where to append results
    twid: to be used to calculate twiddle
    
    recursively apply dif fft blocks
    resuls are in bit reverse order
    '''
    
    xrange = int(N/2) 
    
    
    if N == 1:
        
        outarray.append(inarray[0])
        return
    
    
    ###twiddle function has changed
    def twiddle(x,point): 
        return np.exp(-1j*(2*np.pi/point)*x)   
    
    upper_half = np.zeros((xrange,),dtype=np.complex_)
    lower_half = np.zeros((xrange,),dtype=np.complex_)
    
    
    ###lower half implementation has also changed
    for i in range(0,xrange):
        upper_half[i] = inarray[i]+inarray[i+xrange]
        lower_half[i] = (inarray[i]-inarray[i+xrange])*twiddle(i*(twid/N),twid)
     
            
    radix2(upper_half,xrange,outarray,twid)
    radix2(lower_half,xrange,outarray,twid)

    
    
#### additional reverse function to find bit reverse of a given number
def reverse(num, bitlen):
    ####number: number to be reversed,bitlen: bit length
    result = 0
    for i in range(bitlen):
        if (num >> i) & 1: result |= 1 << (bitlen - 1 - i)
    return result


def reverse_bits(inarray,point,bitlen):
    '''
    input array
    number of points 
    bit length
    '''
    outarray = np.zeros((point,),dtype=np.complex_)
    for i in range(point):
        outarray[i] = inarray[reverse(i,bitlen)]
    return outarray

def my_fft(inarray):
    radix_result = []
    return_arr = np.zeros((256,),dtype=np.complex_)
    radix2(inarray,256,radix_result,256)
    return_arr = reverse_bits(radix_result,256,8)
    return return_arr

def radix2_plot(radix_out,sampling_rate,in_title):
    n = len(radix_out)
    
    yf = radix_out
    xf = np.linspace(0.0,int(sampling_rate/2),int(n/2))
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0/n * np.abs(yf[:int(n//2)]))
    plt.grid()
    plt.title(in_title)
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')
    return plt.show()


# In[39]:


def convolve_256(x,h):
    
    ''' 
    FFT of window is slide over the audio and, multiplied with 
    FFT of each distinct 256-point parts of audio.
    This computation will result to convolution of Fourier domain.
    '''
    
    lenX = len(x) 
    lenH = len(h)

    size = math.floor(lenX/lenH)
    
    fft_h = my_fft(h)
    
    


    conv = np.zeros((size,),dtype=complex) ## holds average values of window multiplications
    temp = np.zeros((lenH,),dtype=complex) ## holds shifted windows of the signal



    for i in range(size):
        temp = x[(i*lenH):(i*lenH)+lenH]
    
        fft_x = my_fft(temp)
        tempVal = np.average(np.multiply(fft_x,fft_h)) #multiply two FFT's
        conv[i] = tempVal 
        

    return conv


# In[40]:


#rate: 44100
#audio = 53.51823129251701 sn




####for second 10 
#### second 10 starts at index = rate * 10

samp1 = rate * 10
print("second 10 index starts: ",samp1)

block1 = math.ceil(samp1/256)
print("block number: ", block1)

index1 = block1*256
print("second 10 index should now start at: ", index1)


print("################")

####for second 20 
#### second 20 starts at index = rate * 20

samp2 = rate * 20
print("second 20 index starts: ",samp2)
block2 = math.ceil(samp2/256)
print("block number: ", block2)

index2 = block2*256
print("second 20 index should now start at: ", index2)


print("################")

####for second 30 
#### second 30 starts at index = rate * 30

samp3 = rate * 30
print("second 30 index starts: ",samp3)
block3 = math.ceil(samp3/256)
print("block number: ",block3)

index3 = block3*256
print("second 30 index should now start at: ", index3)


# In[41]:


####windows' shifted

#10 second window
winFirst = np.zeros((256,))
winFirst = samples[index1:index1+256]

#20 second window
winSec = np.zeros((256,))
winSec = samples[index2:index2+256]

#30 second window
winThird = np.zeros((256,))
winThird = samples[index3:index3+256]



# In[42]:


###result for 10 second case
sec10 = convolve_256(samples,winFirst)

###result for 10 second case
sec20 = convolve_256(samples,winSec)

###result for 30 second case
sec30 = convolve_256(samples,winThird)



# In[43]:


abs10 = abs(sec10) ###take magnitude for plotting 
abs20 = abs(sec20)
abs30 = abs(sec30)



fig = plt.figure(figsize=(20,5))
plt.plot(abs10)
plt.title("10 sec")
plt.xlabel('time in seconds')
plt.ylabel('Amplitude')
plt.show()

fig = plt.figure(figsize=(20,5))
plt.plot(abs20)
plt.title("20 sec")
plt.xlabel('time in seconds')
plt.ylabel('Amplitude')
plt.show()

fig = plt.figure(figsize=(20,5))
plt.plot(abs30)
plt.title("30 sec")
plt.xlabel('time in seconds')
plt.ylabel('Amplitude')
plt.show()


# In[33]:


#part b

b_10 = abs10[block1-200:block1+201]
b_20 = abs20[block2-200:block2+201]
b_30 = abs30[block3-200:block3+201]

fig = plt.figure(figsize=(20,5))
plt.plot(b_10)
plt.title("10 sec")
plt.xlabel('time in seconds')
plt.ylabel('Amplitude')
plt.show()

fig = plt.figure(figsize=(20,5))
plt.plot(b_20)
plt.title("20 sec")
plt.xlabel('time in seconds')
plt.ylabel('Amplitude')
plt.show()

fig = plt.figure(figsize=(20,5))
plt.plot(b_30)
plt.title("30 sec")
plt.xlabel('time in seconds')
plt.ylabel('Amplitude')
plt.show()


# In[29]:


##### additionally the convolusion behaviour in frequency domain 
radix2_plot(sec10,rate,"sec 10 frequency")
radix2_plot(sec20,rate,"sec 20 frequency")
radix2_plot(sec30,rate,"sec 30 frequency")


# In[30]:


##### additionally the convolusion behaviour in frequency domain, for +200,-200 windows
radix10 = sec10[block1-200:block1+201]
radix20 = sec20[block2-200:block2+201]
radix30 = sec30[block3-200:block3+201]
radix2_plot(radix10,rate,"sec 10 frequency +200 -200")
radix2_plot(radix20,rate,"sec 20 frequency +200 -200")
radix2_plot(radix30,rate,"sec 30 frequency +200 -200")


# In[ ]:




