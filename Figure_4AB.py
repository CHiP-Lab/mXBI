# -*- coding: utf-8 -*-
"""
This script generates plots and tables related to Figure 2 of the manuscript:

"Flexible auditory training, psychophysics, and enrichment
of common marmosets with an automated, touchscreen-based system"

by Calapai A.*, Cabrera-Moreno J.*, Moser T., Jeschke M.

* shared contribution

script author: Calapai A. (acalapai@dpz.eu)

February 2022

list of output files:
- Figure_4A.pdf, Figure_4A.png
- Figure_4B.pdf, Figure_4B.png

"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.io import wavfile
import os
import glob

# =============================================
# Setting plotting parameters
sizeMult = 1
saveplot = 0  # 1 or 0; 1 saves plots in the folder "./analysis_output" without showing them; 0 shows without plotting
savetable = 0  # 1 or 0; 1 saves tables in "./analysis_output" without showing them

labelFontSize = 6

sns.set(style="whitegrid")
sns.set_context("paper")

# =============================================
# Parameters for the analysis
CRT_minimumTrials = 50
CRT_minimumTrials_TS = 3000
sliding_window_size = 300
bin_size = 10

pd.options.mode.chained_assignment = None

# =============================================
# Load color palette from animals metadata file
# Assign unique identifier to animals based on the AnimalDictionary.csv

csv_file = './data/Animals_metaData.csv'
AnimalDictionary = pd.read_csv(csv_file, low_memory=False, sep=';')
palette = pd.DataFrame()
for m in AnimalDictionary.monkey.unique():
    palette = palette.append({
        'animal': AnimalDictionary[AnimalDictionary.monkey == m].ID.to_list()[0],
        'color': [AnimalDictionary[AnimalDictionary.monkey == m]['palette_r'].values[0],
                  AnimalDictionary[AnimalDictionary.monkey == m]['palette_g'].values[0],
                  AnimalDictionary[AnimalDictionary.monkey == m]['palette_b'].values[0]]},
        ignore_index=True)

# Create unique palette for each animal
sns.set_palette(sns.color_palette("deep", n_colors=14))
palette = dict(zip(palette.animal, palette.color))

# =============================================
# Plot frequency content and amplitude of the acoustic stimuli
# Panel A: Plot the spectrogram of the acoustic stimuli
if saveplot:
    # Locate the sound folder
    sounds_path = Path('./audio_files/')
    sounds = glob.glob(os.path.join(sounds_path, '*.wav'))

    # Prepare the figure
    figure4A_height = (60 / 25.4) * sizeMult
    figure4A_width = (180 / 25.4) * sizeMult

    f, ax = plt.subplots(2, 5, sharey=False, sharex=False, constrained_layout=False,
                         figsize=(figure4A_width, figure4A_height))

    # Make the subplot handles flat so that they can be cycled through linearly
    ax = ax.ravel()

    # Plot each sound
    for s in range(0, len(sounds)):
        samplingFrequency, signalData = wavfile.read(sounds[s])
        ax[s].set_title(sounds[s].split(os.sep)[1][0:-1 - 3], fontsize=labelFontSize)

        ax[s].plot(signalData)
        ax[s + 5].specgram(signalData, Fs=samplingFrequency, cmap='jet')

        if s + 5 == 5:
            ax[s + 5].set_ylabel('Frequency', fontsize=labelFontSize)
            ax[s + 5].set_xlabel('Time', fontsize=labelFontSize)

        if s == 0:
            ax[s].set_ylabel('Amplitude', fontsize=labelFontSize)

    plt.savefig('./analysis_output/Figure_4A.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_4A.png', format='png')
    plt.close()


# Load the data
def dataload():
    performance_df = pd.read_csv('./data/Figure_3C.csv', low_memory=False, decimal=',')

    # Format the columns of the imported curated data file
    performance_df['p_trials'] = performance_df['p_trials'].astype(int)
    performance_df['HitRate'] = performance_df['HitRate'].astype(float)

    return performance_df


# =============================================
# load the data
performance_df = dataload()

# Plot the hit rate across tasks and animals
figure4B_height = (176 / 25.4) * sizeMult
figure4B_width = (74 / 25.4) * sizeMult

# Initialize the figure
f, ax = plt.subplots(4, 1, constrained_layout=False, figsize=(figure4B_width, figure4B_height))
ax = ax.ravel()

# Create a list of all tasks and stimuli
tasks_name = ["Twitter vs Tone", "Phee vs Tone", "White Noise vs Twitter", "Juvenile vs Twitter"]
tasks_list = ["['twitter','puretone']", "['phee','puretone']", "['wnoise','twitter']", "['infant','twitter']"]

# Create e dataframe for plotting
plot_df = performance_df.copy(deep=False)

# Filter out animals without the minimum amount of trials required for plotting
plot_df = plot_df[plot_df['Trials'] > CRT_minimumTrials]

# Prepare the size range for the line thickness of the line plot
sizes = (min(plot_df.Trials.values), max(plot_df.Trials.values))
size_thick = (1, 3)

# Cycle through each task
for t in range(0, len(tasks_list)):

    # Plot the hit rate across percentage of trials
    g = sns.lineplot(x="p_trials", y="HitRate", size='Trials', hue="animal", palette=palette, sizes=size_thick,
                     ax=ax[t], data=plot_df[plot_df['task'] == tasks_list[t]], legend='brief')
    g.set(ylim=[0, 1.01], ylabel='Hit Rate', xlabel='Trials', title=tasks_list[t])

    if t == 0:
        ax[t].set_title(tasks_name[t], fontsize=labelFontSize)
        ax[t].set(xlabel=None)
        ax[t].set_xticklabels([])
        ax[t].tick_params(labelsize=labelFontSize)
        ax[t].set_ylabel(ylabel='Hit Rate', fontsize=labelFontSize)
        idx = [6, 7, 9, 11]

    if t == 1:
        ax[t].set_title(tasks_name[t], fontsize=labelFontSize)
        ax[t].set(xlabel=None)
        ax[t].set_xticklabels([])
        ax[t].tick_params(labelsize=labelFontSize)
        ax[t].set_ylabel(ylabel='Hit Rate', fontsize=labelFontSize)
        idx = [5, 6, 8, 10]

    if t == 2:
        ax[t].set_title(tasks_name[t], fontsize=labelFontSize)
        ax[t].set(xlabel=None)
        ax[t].set_xticklabels([])
        ax[t].tick_params(labelsize=labelFontSize)
        ax[t].set_ylabel(ylabel='Hit Rate', fontsize=labelFontSize)
        idx = [6, 7, 9, 11]

    if t == 3:
        idx = [5, 6, 8, 11]
        ax[t].set_title(tasks_name[t], fontsize=labelFontSize)
        ax[t].tick_params(labelsize=labelFontSize)
        ax[t].set_ylabel(ylabel='Hit Rate', fontsize=labelFontSize)
        ax[t].set_xlabel(xlabel='Percentage of Trials', fontsize=labelFontSize)

    ax[t].set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax[t].set_xticks([0, 25, 50, 75, 100])
    ax[t].set(ylim=[0, 1])
    ax[t].axhline(0.5, color='grey', linestyle='--')

    handles, labels = ax[t].get_legend_handles_labels()
    l = []
    h = []
    for i in idx:
        l.append(labels[i])
        h.append(handles[i])
    g.legend(h, l, loc='lower center', ncol=2, columnspacing=0.5, frameon=True, title=None, fontsize=labelFontSize)

plt.tight_layout()

# Save the plot
if saveplot:
    plt.savefig('./analysis_output/Figure_4B.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_4B.png', format='png')
    plt.close()
