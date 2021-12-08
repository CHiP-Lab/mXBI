# -*- coding: utf-8 -*-
"""
This script generates plots and tables related to Figure 2 of the manuscript:

"Flexible auditory training, psychophysics, and enrichment
of common marmosets with an automated, touchscreen-based system"

by Calapai A.*, Cabrera-Moreno J.*, Moser T., Jeschke M.

* shared contribution

script author: Calapai A. (acalapai@dpz.eu)

December 2021

list of output files:
- Figure_2.txt, Figure_2.csv:
- Figure_2A.pdf , Figure_2A.png
- Figure_2B.pdf , Figure_2B.png

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================
# Setting plotting parameters
sizeMult = 1
saveplot = 0  # 1 or 0; 1 saves plots in the folder "./analysis_output" without showing them; 0 shows without plotting
savetable = 0  # 1 or 0; 1 saves tables in "./analysis_output" without showing them

tickFontSize = 8
labelFontSize = 10
titleFontSize = 10

sns.set(style="whitegrid")
sns.set_context("paper")

# =============================================
# Parameters for the analysis
CRT_minimumTrials = 100
CRT_minimumTrials_TS = 3000

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
# Load the data for Figure 2

def dataload_corrected():
    corrected_df = pd.read_csv('./data/Figure_2_correctedDF.csv', low_memory=False, decimal=',')

    # Format the columns of the imported curated data file
    corrected_df['trial'] = corrected_df['trial'].astype('int32')
    corrected_df['step'] = corrected_df['step'].astype('int32')
    corrected_df['p_trial'] = corrected_df['p_trial'].astype(float)

    return corrected_df


def dataload_AUT():
    AUT_df = pd.read_csv('./data/Figure_2_AUTdf.csv', low_memory=False, decimal=',')

    # Format the columns of the imported curated data file
    AUT_df['hitrate'] = AUT_df['hitrate'].astype(float)
    AUT_df['step'] = AUT_df['step'].astype('int32')
    AUT_df['total_trials'] = AUT_df['total_trials'].astype('int32')
    AUT_df['sessions'] = AUT_df['sessions'].astype('int32')
    AUT_df['reward'] = AUT_df['reward'].astype('int32')

    return AUT_df


# =============================================
# FIGURE 2A
figure2A_height = (120 / 25.4) * sizeMult
figure2A_width = (80 / 25.4) * sizeMult

# load the data
corrected_df = dataload_corrected()
AUT_df = dataload_AUT()

sns.set_palette(sns.color_palette("Set2", n_colors=len(AUT_df.milestone.unique())))
milestone_palette = dict(zip(AUT_df.milestone.unique(), sns.color_palette()))
milestone_palette.update({"milestone": "k"})

corrected_df['Trials'] = corrected_df['total_trials']
corrected_df['Animal'] = corrected_df['monkey']

# initialize figure
f, ax = plt.subplots(2, 1, constrained_layout=True, figsize=(figure2A_width, figure2A_height))

# plot hit rate across steps
g = sns.barplot(x="step", y="hitrate", data=AUT_df, hue='milestone', palette=milestone_palette,
                ci=95, edgecolor='k', linewidth=0, errwidth=1, dodge=False, ax=ax[0])

# aesthetics
ax[0].legend(loc='lower center', columnspacing=0.4, handletextpad=0.05, ncol=4, prop={'size': 8})
ax[0].set_ylabel(ylabel='Hit Rate')
ax[0].set_xlabel(xlabel='AUT Steps', fontsize=labelFontSize)
ax[0].set(xlim=[-1, 48])
ax[0].set_xticks([0, 14, 29, 44])
ax[0].set_yticks(ax[0].get_yticks()[:-1])

# plot hit rate across percentage of trials
sizes = [min(AUT_df.total_trials.values), max(AUT_df.total_trials.values)]
size_thick = (2, 4)
g = sns.lineplot(x='p_trial', y='step', hue='Animal', size='Trials', sizes=size_thick,
                 alpha=1, palette=palette, data=corrected_df, ax=ax[1])

# aesthetics
ax[1].legend(ncol=2, prop={'size': 7}, columnspacing=-1)
ax[1].set(xlim=[-1, 101], ylim=[0, 51])
ax[1].set_yticks([2, 10, 20, 30, 40, 49])
ax[1].set_xlabel(xlabel='Percentage of trials', fontsize=labelFontSize)
ax[1].set_ylabel(ylabel='AUT steps', fontsize=labelFontSize)
ax[1].tick_params(labelsize=tickFontSize)

ax[1].axhspan(ymin=2, ymax=17, facecolor=milestone_palette['size'], alpha=0.2)
ax[1].axhspan(ymin=17, ymax=32, facecolor=milestone_palette['position'], alpha=0.2)
ax[1].axhspan(ymin=32, ymax=46, facecolor=milestone_palette['sound'], alpha=0.2)
ax[1].axhspan(ymin=46, ymax=49, facecolor=milestone_palette['distractor'], alpha=0.2)

# save the plot
if saveplot:
    plt.savefig('./analysis_output/Figure_2A.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_2A.png', format='png')
    plt.close()

# =============================================
# Assign the milestone labels to the corrected dataframe
corrected_df.loc[corrected_df['step'] <= 15, 'milestone'] = 'size'
corrected_df.loc[(corrected_df['step'] > 15) & (corrected_df['step'] <= 30), 'milestone'] = 'position'
corrected_df.loc[(corrected_df['step'] > 30) & (corrected_df['step'] <= 45), 'milestone'] = 'sound'
corrected_df.loc[corrected_df['step'] > 45, 'milestone'] = 'distractor'

# Compute the percentage of trials each animal spent on each milestone
AUT_range = pd.DataFrame()
for m in corrected_df.monkey.unique():
    for ml in corrected_df.milestone.unique():

        # calculate the range of percentage of trials in the selected milestone for the selected animal
        ran = corrected_df[(corrected_df['monkey'] == m) & (corrected_df['milestone'] == ml)]['p_trial'].max() - \
              corrected_df[(corrected_df['monkey'] == m) & (corrected_df['milestone'] == ml)]['p_trial'].min()

        # count the trials
        tot = len(corrected_df[(corrected_df['monkey'] == m) & (corrected_df['milestone'] == ml)])

        if tot == 0:
            tot = np.nan

        # count the sessions
        ses = len(corrected_df[(corrected_df['monkey'] == m) &
                               (corrected_df['milestone'] == ml)]['sessionNumber'].unique())
        if ses == 0:
            ses = np.nan

        AUT_range = AUT_range.append({
            'animal': m,
            'trials': tot,
            'sessions': ses,
            'range': ran,
            'milestone': ml},
            ignore_index=True)

# ========================================================================================================
# Panel B: Trials, Session, Percentage of Trials as a function of milestones across the 4 animals
figure2B_height = (120 / 25.4) * sizeMult
figure2B_width = (40 / 25.4) * sizeMult

# initialize the figure
f, ax = plt.subplots(3, 1, constrained_layout=True, sharex=True, figsize=(figure2B_width, figure2B_height))

# plot the trials across milestones
g = sns.stripplot(x='milestone', y='trials', dodge=True, data=AUT_range, color='gray', ax=ax[0])
g = sns.stripplot(x=AUT_range.groupby(['milestone'], sort=False)['trials'].mean().index,
                  y=AUT_range.groupby(['milestone'], sort=False)['trials'].mean().values,
                  data=AUT_range, color='black', marker='+', linewidth=1, s=8, ax=ax[0])

ax[0].set_xlabel(xlabel=None)
ax[0].set_xticks([])
ax[0].set_ylabel(ylabel='Trials')
ax[0].yaxis.set_ticks_position('right')
ax[0].yaxis.set_label_position("right")

# plot number of sessions across milestones
g = sns.stripplot(x='milestone', y='sessions', dodge=True, data=AUT_range, color='gray', ax=ax[1])
g = sns.stripplot(x=AUT_range.groupby(['milestone'], sort=False)['sessions'].mean().index,
                  y=AUT_range.groupby(['milestone'], sort=False)['sessions'].mean().values,
                  data=AUT_range, color='black', marker='+', linewidth=1, s=8, ax=ax[1])

ax[1].set_ylabel(ylabel='Sessions')
ax[1].set_xlabel(xlabel=None)
ax[1].set_xticks([])
ax[1].yaxis.set_ticks_position('right')
ax[1].yaxis.set_label_position("right")

# plot range of trials across milestones
g = sns.stripplot(x='milestone', y='range', dodge=True, data=AUT_range, color='gray', ax=ax[2])
g = sns.stripplot(x=AUT_range.groupby(['milestone'], sort=False)['range'].mean().index,
                  y=AUT_range.groupby(['milestone'], sort=False)['range'].mean().values,
                  data=AUT_range, color='black', marker='+', linewidth=1, s=8, ax=ax[2])

ax[2].tick_params(axis='x', rotation=90)
ax[2].set_ylabel(ylabel='Percentage of Trials')
ax[2].set_xlabel(xlabel=None)
ax[2].yaxis.set_ticks_position('right')
ax[2].yaxis.set_label_position("right")

for i in range(0, 3):
    ax[i].axvspan(xmin=-0.3, xmax=0.3, facecolor=milestone_palette['size'], alpha=0.2)
    ax[i].axvspan(xmin=0.7, xmax=1.3, facecolor=milestone_palette['position'], alpha=0.2)
    ax[i].axvspan(xmin=1.7, xmax=2.3, facecolor=milestone_palette['sound'], alpha=0.2)
    ax[i].axvspan(xmin=2.7, xmax=3.3, facecolor=milestone_palette['distractor'], alpha=0.2)

# compute median information
AUT_medians = pd.DataFrame()
medians = ['trials', 'sessions', 'range']
for ml in corrected_df.milestone.unique():
    for md in medians:
        median_value = AUT_range[AUT_range['milestone'] == ml][md].median()

        AUT_medians = AUT_medians.append({
            'milestone': ml,
            'value': int(median_value),
            'median': md},
            ignore_index=True)

AUT_medians['value'] = AUT_medians['value'].astype(int)

# Save the plot
if saveplot:
    plt.savefig('./analysis_output/Figure_2B.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_2B.png', format='png')
    plt.close()

# save table
if savetable:
    AUT_medians.to_csv(r'./analysis_output/Figure_2.csv', sep=',', index=False)
    AUT_medians.to_csv(r'./analysis_output/Figure_2.txt', sep=',', index=False)
