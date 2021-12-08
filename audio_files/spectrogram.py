# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:51:13 2020

@author: Jorge Cabrera-Moreno

Marmoset spectrogram
"""


import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

# Read the wav file (mono)
sounds = ['/Users/acalapai/ownCloud/Shared/mXBI_manuscript/audio_voc/mv003.wav']
for s in sounds:
    samplingFrequency, signalData = wavfile.read(s)


    # Plot the signal read from wav file
    plt.subplot(211)
    plt.title('Spectrogram of a baby marmoset call')


    # signalData = signalData[:-114]
    # print(f'signal data: {signalData}')
    # print(f'lenght signal data: {len(signalData)}')

    # print(f'sampling Freq: {samplingFrequency}')

    plt.plot(signalData)
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.xlim(0,100000)


    plt.subplot(212)
    plt.specgram(signalData,Fs=samplingFrequency, cmap='jet')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    # Computes the power of spectral density (PSD)
    freqs, psd = signal.welch(signalData)

    plt.figure(figsize=(5, 4))
    plt.semilogx(freqs, psd)
    plt.title('PSD: power spectral density')
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.tight_layout()

    plt.show()

