# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:51:13 2020

@author: Jorge Cabrera-Moreno

Marmoset spectrogram
"""


import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy import signal

# Read the wav file (mono)
sounds = 'clip5_MS.wav'
    # r'C:\Users\jmoreno\Desktop\clipsMS\clip5_MS.wav',]
    # r'Y:\home\jcabreramoreno\code\python\programs\toneGenerator\monoTones\tones\PureTone_Ramped_4000.wav']
    # r'Y:\home\jcabreramoreno\data\superDF\vocs\1500c100_mono.wav']
for s in sounds:
    samplingFrequency, signalData = wavfile.read(s)
     
    
    # Plot the signal read from wav file
    plt.subplot(211)
    plt.title('Spectrogram ')
    
    
    # signalData = signalData[:-114]
    # print(f'signal data: {signalData}')
    # print(f'lenght signal data: {len(signalData)}')
    
    # print(f'sampling Freq: {samplingFrequency}')
    
    plt.plot(signalData)
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    # plt.xlim(0,15000)
    
    
    plt.subplot(212)
    plt.specgram(signalData,Fs=samplingFrequency, cmap='jet')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    
    # Computes the power of spectral density (PSD)
    freqs, psd = signal.welch(signalData)
    
    plt.figure(figsize=(5, 4))
    plt.plot(freqs*samplingFrequency, 10*np.log10(psd))
    plt.title('PSD: power spectral density')
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.tight_layout()
    
    plt.show()

