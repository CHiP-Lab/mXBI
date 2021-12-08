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
- Figure_3A.pdf , Figure_3A.png

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================
# disable chain assignment warning
pd.options.mode.chained_assignment = None  # default='warn'

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
CRT_minimumTrials_2AC = 500
CRT_minimumTrials_TS = 3000
CTRL_lastNsessions = 10

CTRL_RT_min = 0.4  # in milliseconds
CTRL_RT_max = 5  # in milliseconds

sliding_window_size = 100  # in trials
bin_size = 5

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
# Load the data for Figure 3A

def dataload():
    performance_df = pd.read_csv('./data/Figure_3A.csv', low_memory=False, decimal=',')

    # Format the columns of the imported curated data file
    performance_df['p_trials'] = performance_df['p_trials'].astype(int)
    performance_df['HitRate'] = performance_df['HitRate'].astype(float)
    performance_df['Trials'] = performance_df['Trials'].astype(int)

    return performance_df


# ========================================================
# FIGURE 3A
figure3A_height = (90 / 25.4) * sizeMult
figure3A_width = (180 / 25.4) * sizeMult

# load the data
performance_df = dataload()
plot_df = performance_df.groupby(['sessionType', 'monkey', 'p_trials', 'Trials'])['HitRate'].mean().reset_index()

# initialize the figure
f, (ax1, ax2) = plt.subplots(1, 2, sharey=False, gridspec_kw={'width_ratios': [1, 1, ]},
                             constrained_layout=False, figsize=(figure3A_width, figure3A_height))

# Plot the Natural Discrimination, 3 Visual Stimuli condition
sizes = (min(performance_df[performance_df['sessionType'] == '2 Visual Stimuli'].Trials.values),
         max(performance_df[performance_df['sessionType'] == '2 Visual Stimuli'].Trials.values))

size_thick = (2, 4)
g = sns.lineplot(x="p_trials", y="HitRate", size='Trials', sizes=size_thick, hue="monkey", legend='brief',
                 data=plot_df[plot_df['sessionType'] == '2 Visual Stimuli'], ax=ax1, palette=palette)

g.set(ylim=[0, 1], ylabel='Hit Rate', xlabel='Percentage of Trials', title='2 Visual Stimuli')
g.set(xlim=[0, 100])

# Manually create a legend for the total trial
handles, labels = [(a + b) for a, b, in zip(ax1.get_legend_handles_labels(), ax2.get_legend_handles_labels())]
idx = [10, 11, 12, 13, 14, 15]

l = []
h = []

for i in idx:
    l.append(labels[i])
    h.append(handles[i])

l[0] = 'Trials'
g.legend(h, l, loc='lower center', ncol=2, frameon=False, title=None)

ax1.set_yticks([0.25, 0.5, 0.75, 1])
ax1.axhline(0.50, color='grey', linestyle='--')
ax1.tick_params(axis=u'both', which=u'both', length=0)

# Plot the Natural Discrimination, 3 Visual Stimuli condition
sizes = (min(plot_df[plot_df['sessionType'] == '3 Visual Stimuli'].Trials.values),
         max(plot_df[plot_df['sessionType'] == '3 Visual Stimuli'].Trials.values))

size_thick = (2, 3.5)

g = sns.lineplot(x="p_trials", y="HitRate", size='Trials', sizes=size_thick, hue="monkey", legend='brief',
                 data=plot_df[plot_df['sessionType'] == '3 Visual Stimuli'], ax=ax2, palette=palette)

g.set(ylim=[0, 1], ylabel=None, xlabel='Percentage of Trials', title='3 Visual Stimuli')
g.set(xlim=[0, 100])
ax2.set_yticks([0.16, 0.33, 0.5, 0.66, 0.82, 1])
ax2.axhline(0.33, color='grey', linestyle='--')

handles, labels = [(a + b) for a, b, in zip(ax1.get_legend_handles_labels(), ax2.get_legend_handles_labels())]
idx = [21, 22, 23, 24, 25]

l = []
h = []

for i in idx:
    l.append(labels[i])
    h.append(handles[i])

l[0] = 'Trials'
g.legend(h, l, loc='lower center', ncol=2, frameon=False, title=None)

# Add figure level legend for the animal names
ax3 = ax2.twinx()
ax3.get_yaxis().set_visible(False)
ax3.set_yticklabels([])
ax2.tick_params(axis=u'both', which=u'both', length=0)

handles, labels = [(a + b) for a, b, in zip(ax1.get_legend_handles_labels(), ax2.get_legend_handles_labels())]
idx = [0, 1, 2, 3, 4, 5, 6, 17, 18, 7, 8, 9]

l = []
h = []

for i in idx:
    l.append(labels[i])
    h.append(handles[i])

l[0] = 'Animals'
ax3.legend(h, l, loc='center right', bbox_to_anchor=(1.33, 0.5), ncol=1, frameon=False, title=None, fontsize='small')

# Save the figure
if saveplot:
    plt.savefig('./analysis_output/Figure_3A.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_3A.png', format='png')
    plt.close()
