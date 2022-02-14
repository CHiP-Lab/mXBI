# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:51:13 2020

@author: Jorge Cabrera-Moreno, Antonino Calapai

Marmoset spectrogram
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy import signal
from pathlib import Path
import os

# Read the wav file (mono)
file_path = "./background_recordings/'
save_path = "./analysis_output/

sounds = [ os.path.join(file_path, 'clip1_MS.wav'),
           os.path.join(file_path, 'clip2_MS.wav'),
           os.path.join(file_path, 'clip3_MS.wav')]

for idx, s in enumerate(sounds):
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

    filename = "{}{}{}{}{}{}".format(save_path, '/', 'Figure_5C', '_spectrogram_', idx+1, '.pdf')
    plt.savefig(filename, format='pdf')
    plt.close()

    # Computes the power of spectral density (PSD)
    freqs, psd = signal.welch(signalData)
    
    plt.figure(figsize=(5, 4))
    plt.plot(freqs*samplingFrequency, 10*np.log10(psd))
    plt.title('PSD: power spectral density')
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.tight_layout()
    
    plt.show()

    filename = "{}{}{}{}{}{}".format(save_path, '/', 'Figure_5C', '_PSD_', idx+1, '.pdf')
    plt.savefig(filename, format='pdf')
    plt.close()
