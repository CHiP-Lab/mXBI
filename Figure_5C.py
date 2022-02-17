# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:51:13 2020

@author: Jorge Cabrera-Moreno, Antonino Calapai

Marmoset spectrogram

list of input files:
- PSD_data.csv
- clip1_MS.wav
- clip2_MS.wav
- clip3_MS.wav

list of output files:
- Figure_5C_PSD_1.pdf
- Figure_5C_PSD_2.pdf
- Figure_5C_PSD_3.pdf
- Figure_5C_spectrogram_1.pdf
- Figure_5C_spectrogram_2.pdf
- Figure_5C_spectrogram_3.pdf

"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.io import wavfile
import os

# Read the wav file (mono)
file_path = "./background_recordings/"
save_path = "./analysis_output/"

sounds = [ os.path.join(file_path, 'clip1_MS.wav'),
           os.path.join(file_path, 'clip2_MS.wav'),
           os.path.join(file_path, 'clip3_MS.wav')]

psdData = './data/PSD_data.csv'

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
           
           

# Power spectral desity plot
psdDF = pd.read_csv(psdData)
plt.figure(figsize=(5, 4))
plt.plot(psdDF['freq'], psdDF['power'])
plt.title('PSD: power spectral density')
plt.xlabel('Frequency')
plt.ylabel('Power')
plt.tight_layout()

filename = "{}{}{}{}".format(save_path, '/', 'Figure_5C','_PSD.pdf')
plt.savefig(filename, format='pdf')
plt.close()
