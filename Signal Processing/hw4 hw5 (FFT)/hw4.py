#!/usr/bin/env python
# coding: utf-8

# In[336]:


###Ekin Celebi
###150160152
###### Africa.wav = 0db gain raw
###### Africa5db.wav = 5db gain raw
###### AfricaLPF0db.wav = 0db gain lpf
###### AfricaLPF5db.wav = 5db gain lpf
###### dive link for audio files
####https://drive.google.com/drive/folders/1_EHKsR-wilJGP8VwR4q60-tLOpIj20Zy?usp=sharing

# In[ ]:


import pandas
import numpy as np
import matplotlib.pyplot as plt
import librosa as librosa
samples, rate = librosa.load('Africa.wav',sr=None,mono=True,offset =0.0,duration=None)
samples5gain, rate5gain = librosa.load('Africa5db.wav',sr=None,mono=True,offset =0.0,duration=None)


# In[337]:


sample_lpf_0, rate0 = librosa.load('AfricaLPF0db.wav',sr=None,mono=True,offset =0.0,duration=None)
sample_lpf_5, rate5 = librosa.load('AfricaLPF5db.wav',sr=None,mono=True,offset =0.0,duration=None)


# In[338]:


from IPython.display import Audio
Audio('Africa.wav')


# In[339]:


Audio('Africa5db.wav')


# In[340]:


Audio('AfricaLPF0db.wav')


# In[341]:


Audio('AfricaLPF5db.wav')


# In[342]:


from librosa import display
plt.figure()

librosa.display.waveplot(y=samples5gain,sr=rate5gain)
librosa.display.waveplot(y=samples,sr=rate)
plt.xlabel('time in seconds')
plt.ylabel('Amplitude')
plt.show()


# In[343]:



'''
Fourier Transform is a mathematical concept that can
decompose a signal into its constituent frequencies
'''


# In[375]:


'''
first 256 signals of a given time = (sample_rate*t)+i
i = 0,....,255
'''

ten_second_samples = np.zeros((256,))
for i in range(256):
    ten_second_samples[i] = samples[(10*rate)+i]
    
twenty_second_samples = np.zeros((256,))
for i in range(256):
    twenty_second_samples[i] = samples[(20*rate)+i]

thirty_second_samples = np.zeros((256,))
for i in range(256):
    thirty_second_samples[i] = samples[(30*rate)+i]


# In[376]:


ten_second_samples5gain = np.zeros((256,))
for i in range(256):
    ten_second_samples5gain[i] = samples5gain[(10*rate)+i]
    
twenty_second_samples5gain = np.zeros((256,))
for i in range(256):
    twenty_second_samples5gain[i] = samples5gain[(20*rate)+i]

thirty_second_samples5gain = np.zeros((256,))
for i in range(256):
    thirty_second_samples5gain[i] = samples5gain[(30*rate)+i]


# In[377]:


ten_second_0db = np.zeros((256,))
for i in range(256):
    ten_second_0db[i] = sample_lpf_0[(10*rate0)+i]
    
twenty_second_0db = np.zeros((256,))
for i in range(256):
    twenty_second_0db[i] = sample_lpf_0[(20*rate0)+i]

thirty_second_0db = np.zeros((256,))
for i in range(256):
    thirty_second_0db[i] = sample_lpf_0[(30*rate0)+i]


# In[378]:


ten_second_5db = np.zeros((256,))
for i in range(256):
    ten_second_5db[i] = sample_lpf_5[(10*rate5)+i]
    
twenty_second_5db = np.zeros((256,))
for i in range(256):
    twenty_second_5db[i] = sample_lpf_5[(20*rate5)+i]

thirty_second_5db = np.zeros((256,))
for i in range(256):
    thirty_second_5db[i] = sample_lpf_5[(30*rate5)+i]


# In[379]:


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
    
    def twiddle(x,point): 
        return np.exp((-2j*np.pi*x)/point)
    
    upper_half = np.zeros((xrange,),dtype=np.complex_)
    lower_half = np.zeros((xrange,),dtype=np.complex_)
    
    for i in range(0,xrange):
        upper_half[i] = inarray[i]+inarray[i+xrange]
        lower_half[i] = (inarray[i]-inarray[i+xrange])*twiddle(i,twid)
     
            
    radix2(upper_half,xrange,outarray,twid)
    radix2(lower_half,xrange,outarray,twid)


# In[380]:


hold_ten = [] #hold output array
hold_twenty = [] #hold output array
hold_thirty = [] #hold output array

#apply radix two to samples output will be in bit reverse order
#to use 256 point radix2 dif fft take first 256 signal of relevant time(in second)

radix2(ten_second_samples,256,hold_ten,256)
radix2(twenty_second_samples,256,hold_twenty,256)
radix2(thirty_second_samples,256,hold_thirty,256)


# In[381]:


hold_ten_raw5 = [] #hold output array
hold_twenty_raw5 = [] #hold output array
hold_thirty_raw5 = [] #hold output array

#apply radix two to samples output will be in bit reverse order
#to use 256 point radix2 dif fft take first 256 signal of relevant time(in second)

radix2(ten_second_samples5gain,256,hold_ten_raw5,256)
radix2(twenty_second_samples5gain,256,hold_twenty_raw5,256)
radix2(thirty_second_samples5gain,256,hold_thirty_raw5,256)


# In[382]:


#for 0 db gain
hold_ten_0 = [] #hold output array
hold_twenty_0 = [] #hold output array
hold_thirty_0 = [] #hold output array

#apply radix two to samples output will be in bit reverse order
#to use 256 point radix2 dif fft take first 256 signal of relevant time(in second)

radix2(ten_second_0db,256,hold_ten_0,256)
radix2(twenty_second_0db,256,hold_twenty_0,256)
radix2(thirty_second_0db,256,hold_thirty_0,256)


# In[383]:


#for 5 db gain
hold_ten_5 = [] #hold output array
hold_twenty_5 = [] #hold output array
hold_thirty_5 = [] #hold output array

#apply radix two to samples output will be in bit reverse order
#to use 256 point radix2 dif fft take first 256 signal of relevant time(in second)

radix2(ten_second_5db,256,hold_ten_5,256)
radix2(twenty_second_5db,256,hold_twenty_5,256)
radix2(thirty_second_5db,256,hold_thirty_5,256)


# In[384]:


def reverse_bits(inarray,point):
    '''
    takes array and it's length as input
    reverses array to normal order
    returns output array
    '''
    outarray = np.zeros((point,),dtype=np.complex_)
    half = int(point/2)
    for i in range(0,half):
        outarray[2*i] = inarray[i] 
        outarray[(2*i)+1] = inarray[i+half]
    return outarray
    


# In[385]:


out_ten_raw5 = reverse_bits(hold_ten_raw5,256) #reverse bits back to normal
out_twenty_raw5 = reverse_bits(hold_twenty_raw5,256)
out_thirty_raw5 = reverse_bits(hold_thirty_raw5,256)


# In[386]:


out_ten = reverse_bits(hold_ten,256) #reverse bits back to normal
out_twenty = reverse_bits(hold_twenty,256)
out_thirty = reverse_bits(hold_thirty,256)


# In[387]:


out_ten_0 = reverse_bits(hold_ten_0,256) #reverse bits back to normal
out_twenty_0 = reverse_bits(hold_twenty_0,256)
out_thirty_0 = reverse_bits(hold_thirty_0,256)


# In[388]:


out_ten_5 = reverse_bits(hold_ten_5,256) #reverse bits back to normal
out_twenty_5 = reverse_bits(hold_twenty_5,256)
out_thirty_5 = reverse_bits(hold_thirty_5,256)


# In[401]:


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


# In[402]:


###### t = 10s
radix2_plot(out_ten,rate,'t=10 raw data 0 gain') #raw 0 gain
radix2_plot(out_ten_0,rate0,'t=10 lpf data 0 gain') #lpf 0 gain


# In[404]:


###### t = 10s  
radix2_plot(out_ten_raw5,rate5gain,'t=10 raw data 5 gain') #raw 5 gain
radix2_plot(out_ten_5,rate5,'t=10 lpf data 5 gain') #lpf 5 gain


# In[405]:


###### t = 20s  
radix2_plot(out_twenty,rate,'t=20 raw data 0 gain') #raw 0 gain
radix2_plot(out_twenty_0,rate0,'t=20 lpf data 0 gain') #lpf 0 gain


# In[406]:


###### t = 20s  
radix2_plot(out_twenty_raw5,rate5gain,'t=20 raw data 5 gain') #raw 5 gain
radix2_plot(out_twenty_5,rate5,'t=20 lpf data 5 gain') #lpf 5 gain


# In[409]:


###### t = 30s  
radix2_plot(out_thirty,rate,'t=30 raw data 0 gain') #raw 0 gain
radix2_plot(out_thirty_0,rate0,'t=30 lpf data 0 gain') #lpf 0 gain


# In[410]:


###### t = 30s  
radix2_plot(out_thirty_raw5,rate5gain,'t=30 raw data 5 gain') #raw 5 gain
radix2_plot(out_thirty_5,rate5,'t=30 raw data 5 gain') #lpf 0 gain


# In[ ]:


#fourier transfrom allowed us to convert
#continuous signal from time domain to frequency domain


# In[ ]:




