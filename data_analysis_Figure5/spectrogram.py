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
sounds = ['./audio_clips/clip1_MS.wav',
         './audio_clips/clip2_MS.wav',
         './audio_clips/clip3_MS.wav',]

psdData = './data/PSD_data.csv'

# Spectrogram and waveform plots
for s in sounds:
    samplingFrequency, signalData = wavfile.read(s)

    # Plot the signal read from wav file
    plt.figure()
    plt.subplot(211)
    plt.title('Spectrogram ')
    
    plt.plot(signalData)
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    
    plt.subplot(212)
    plt.specgram(signalData,Fs=samplingFrequency, cmap='jet')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    
    plt.show()

# Power spectral demsity plot
plt.figure()
psdDF = pd.read_csv(psdData)
plt.figure(figsize=(5, 4))
plt.plot(psdDF['freq'], psdDF['power'])
plt.title('PSD: power spectral density')
plt.xlabel('Frequency')
plt.ylabel('Power')
plt.tight_layout()

plt.show()
