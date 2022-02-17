# -*- coding: utf-8 -*-
"""
This script generates plots and tables related to Supplementary Figure 3 of the manuscript:

"Flexible auditory training, psychophysics, and enrichment
of common marmosets with an automated, touchscreen-based system"

by Calapai A.*, Cabrera-Moreno J.*, Moser T., Jeschke M.

* shared contribution

script author: Calapai A. (acalapai@dpz.eu)

February 2022

list of input files:
- Figure_S3_ITI_times.csv
- Figure_S3_ITI_summary.csv

list of output files:
- Figure_S3.txt , Figure_S3.csv
- Figure_S3.pdf , Figure_S3.png

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# =============================================
# Setting plotting parameters
sizeMult = 1
saveplot = 1  # 1 or 0; 1 saves plots in the folder "./analysis_output" without showing them; 0 shows without plotting
savetable = 1  # 1 or 0; 1 saves tables in "./analysis_output" without showing them

figureS3_height = (60 / 25.4) * sizeMult
figureS3_width = (180 / 25.4) * sizeMult

# =============================================
# Parameters for the analysis
CRT_minimumTrials = 100

likelihood_window = 30000  # in milliseconds
maximum_ITI = 60000  # in milliseconds
penalty_wrong = 5000  # in milliseconds

histogram_window = 15000  # in milliseconds
histogram_bins = 200  # in milliseconds

tickFontSize = 8
labelFontSize = 10
titleFontSize = 10

sns.set(style="whitegrid")
sns.set_context("paper")

def dataload():
    ITI_times = pd.read_csv('./data/Figure_S3_ITI_times.csv', low_memory=False, decimal='.', sep=';')
    ITI_summary = pd.read_csv('./data/Figure_S3_ITI_summary.csv', low_memory=False, decimal='.', sep=';')

    return ITI_times, ITI_summary


# ==== PLOT
ITI_times, ITI_summary = dataload()
outcomes = ['reward', 'wrong']

figureS3_height = (180 / 25.4) * sizeMult
figureS3_width = (160 / 25.4) * sizeMult

# Initialize a summary dataframe for the statistics
STATS = pd.DataFrame(columns=['monkey', 'n', 'test', 'pvalue'])

# Initialize the figure
manual_list = ['d', 'i', 'k', 'j', 'f', 'c']
g, ax = plt.subplots(len(manual_list), 2, sharex='col', constrained_layout=True,
                     gridspec_kw={'width_ratios': [1, 5]}, figsize=(figureS3_width, figureS3_height))

for m in range(0, len(manual_list)):
    plot_df = ITI_summary[ITI_summary['animal'] == manual_list[m]]
    g = sns.barplot(x="outcome", y="likelihood", data=plot_df, ax=ax[m, 0])

    ax[m, 0].text(0, 1, manual_list[m], color='black', fontsize=14, va="top", ha="right")
    ax[m, 0].set(xlabel=None)
    ax[m, 0].set_yticks([0, .5, 1])
    ax[m, 0].set(ylim=[0, 1])

    # I could not force a order of categories for the outcomes here with histplot, but by turning legend to True in the
    # plot reveals the color code for the outcomes for this plot
    for outcome in outcomes:
        data = ITI_times[(ITI_times['animal'] == manual_list[m]) & (ITI_times['Outcome'] == outcome)]
        ax[m, 1].hist(data.ITI,
                      bins=np.arange(0, histogram_window, histogram_bins),
                      range=[0, histogram_window], alpha=0.5,
                      label=f"{outcome}: n = {len(data)}")

    ax[m, 1].legend()

    # N = len(plot_df[plot_df['animal'] == manual_list[m]])
    # ax[m, 1].text(15, 0, 'N = ' + str(N), color='black', fontsize=8, va="bottom", ha="right")
    # ax[m, 1].set(ylabel=None, xlim=[0, 15])
    # # ax[m, 1].set_xticks([0, 5, 10, 15])

# ====
if saveplot:
    plt.savefig('./analysis_output/Figure_S3.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_S3.png', format='png')
    plt.close()

ITI_times = ITI_times.sort_values(by=['animal', 'ITI'])
ITI_times = ITI_times.reset_index(drop=True)

# ============================================================================================
# show summary statistics
pivoted_mean = ITI_summary.pivot(index='animal', columns='outcome', values='ITI mean').reset_index()
pivoted_std = ITI_summary.pivot(index='animal', columns='outcome', values='ITI std').reset_index()

ITI_summary = pd.DataFrame()
ITI_summary['Animal'] = pivoted_mean['animal']
ITI_summary['Mean Correct'] = pivoted_mean['reward']
ITI_summary['Mean Wrong'] = pivoted_mean['wrong']
ITI_summary['std Correct'] = pivoted_std['reward']
ITI_summary['std Wrong'] = pivoted_std['wrong']

ITI_summary = ITI_summary.append({
    'Animal': 'total',
    'Mean Correct': ITI_summary['Mean Correct'].mean(),
    'Mean Wrong': ITI_summary['Mean Wrong'].mean(),
    'std Correct': ITI_summary['std Correct'].mean(),
    'std Wrong': ITI_summary['std Wrong'].mean()},
    ignore_index=True)

ITI_summary['Mean Correct'] = round(ITI_summary['Mean Correct'], 2)
ITI_summary['Mean Wrong'] = round(ITI_summary['Mean Wrong'], 2)
ITI_summary['std Correct'] = round(ITI_summary['std Correct'], 2)
ITI_summary['std Wrong'] = round(ITI_summary['std Wrong'], 2)

if savetable:
    ITI_summary.to_csv(r'./analysis_output/Figure_S3.txt', sep=';', index=False)
    ITI_summary.to_csv(r'./analysis_output/Figure_S3.csv', sep=';', index=False)
