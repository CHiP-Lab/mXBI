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
sounds = ['./data/clip1_MS.wav',
         './data/clip2_MS.wav',
         './data/clip3_MS.wav',]

for s in sounds:
    samplingFrequency, signalData = wavfile.read(s)

    # Plot the signal read from wav file
    plt.subplot(211)
    plt.title('Spectrogram ')
    
    plt.plot(signalData)
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    
    
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

