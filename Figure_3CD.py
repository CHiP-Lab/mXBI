# -*- coding: utf-8 -*-
"""
This script generates plots and tables related to Figure 3 of the manuscript:

"Flexible auditory training, psychophysics, and enrichment
of common marmosets with an automated, touchscreen-based system"

by Calapai A.*, Cabrera-Moreno J.*, Moser T., Jeschke M.

* shared contribution

script author: Calapai A. (acalapai@dpz.eu)

February 2022

list of input files:
- Animals_metaData.csv
- Figure_3C_dPDF.csv
- Figure_3C_HR.csv
- Figure_3D_Responses.csv

list of output files:
- Figure_3CD.pdf, Figure_3CD.png
- Figure_3CD.csv, Figure_3CD.txt
- Figure_3CD_dPrime.txt, Figure_3CD_dPrime.csv
- Figure_3CD_HR_binomial.txt, Figure_3CD_HR_binomial.csv
- Figure_3CD_RTs.txt, Figure_3CD_RTs.csv

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sps
from statsmodels.stats.multitest import multipletests

# =============================================
# Setting plotting parameters
sizeMult = 1
saveplot = 1  # 1 or 0; 1 saves plots in the folder "./analysis_output" without showing them; 0 shows without plotting
savetable = 1  # 1 or 0; 1 saves tables in "./analysis_output" without showing them

labelFontSize = 6

sns.set(style="whitegrid")
sns.set_context("paper")
# =============================================
# Parameters for the analysis
CRT_minimumTrials = 500
CRT_minimumTrials_TS = 3000
CTRL_lastNsessions = 5

CTRL_RT_min = 0.4  # in milliseconds
CTRL_RT_max = 5  # in milliseconds

sliding_window_size = 100  # in trials
bin_size = 10

pd.options.mode.chained_assignment = None

# =====
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
# Load the data for Figure 3B

def dataload_dpDF():
    dP_df = pd.read_csv('./data/Figure_3C_dPDF.csv', low_memory=False,  sep=';', decimal='.')

    # Format the columns of the imported curated data file
    dP_df['dprime'] = dP_df['dprime'].astype(float)

    return dP_df


def dataload_HR():
    HR = pd.read_csv('./data/Figure_3C_HR.csv', low_memory=False, sep=';', decimal='.')

    # Format the columns of the imported curated data file
    HR['binomial'] = HR['binomial'].astype(float)
    HR['hits'] = HR['hits'].astype(float)
    HR['ignored'] = HR['ignored'].astype(float)
    HR['adjusted_p'] = HR['adjusted_p'].astype(float)

    return HR


def dataload_Responses():
    Responses = pd.read_csv('./data/Figure_3D_Responses.csv', low_memory=False, sep=';', decimal='.')

    # Format the columns of the imported curated data file
    Responses['RT'] = Responses['RT'].astype(float)

    return Responses


# =============================================
# FIGURE 3CD
figure3CD_height = (80 / 25.4) * sizeMult
figure3CD_width = (180 / 25.4) * sizeMult

# load the data
dP_df = dataload_dpDF()
HR = dataload_HR()
Responses = dataload_Responses()

# Initialize a summary dataframe for the statistics
STATS = pd.DataFrame(columns=['monkey', 'n', 'test', 'pvalue'])

# Extract monkey list from the d prime
monkeys_list = dP_df['monkey'].values

# Initialize the figure
g, ax = plt.subplots(2, len(monkeys_list), sharey='row', sharex='col', constrained_layout=True,
                     gridspec_kw={'height_ratios': [1, 2]}, figsize=(figure3CD_width, figure3CD_height))

# Make the subplot handles flat so that they can be cycled through linearly
ax = ax.flatten()

# Cycle through all animals
for m in range(0, len(monkeys_list)):

    # Plot the 2 Visual Stimuli first
    if m < 9:
        plot_df = HR[(HR['monkey'] == monkeys_list[m]) & (HR['task'] == '2 Visual Stimuli')]
        yval = plot_df[plot_df['monkey'] == monkeys_list[m]]['ignored'] + \
               plot_df[plot_df['monkey'] == monkeys_list[m]]['hits']

        # Plot bar plots of hit rates
        g = sns.barplot(x='stimulus', y=yval, color='#7FFF00', order=('str', 'voc'),
                        data=plot_df[plot_df['monkey'] == monkeys_list[m]], ax=ax[m])
        g = sns.barplot(x='stimulus', y='hits', color=palette[monkeys_list[m]], order=('str', 'voc'),
                        data=plot_df[plot_df['monkey'] == monkeys_list[m]], ax=ax[m])

        g.set(ylim=[0, 1], ylabel=None, xlabel=None)

        ax[m].set_yticks([0.25, 0.5, 0.75])
        ax[m].tick_params(labelsize=labelFontSize)
        ax[m].axhline(0.50, color='k', linestyle='--', alpha=0.7)

        if m == 0:
            # g.set(ylabel='Hit rate')
            ax[m].set_ylabel(ylabel='Hit Rate', fontsize=labelFontSize)

        d_prime = float(dP_df[(dP_df['monkey'] == monkeys_list[m]) & (dP_df['task'] == '2 Visual Stimuli')]['dprime'])
        t_trial = int(sum(HR[(HR['monkey'] == monkeys_list[m]) & (HR['task'] == '2 Visual Stimuli')]['N']))
        #t_trial = float(dP_df[(dP_df['monkey'] == monkeys_list[m]) & (dP_df['task'] == '2 Visual Stimuli')]['trials'])

        ax[m].set_title("{}{}{}{}{}".format(monkeys_list[m], "\n", d_prime, '\n', int(t_trial)), fontsize=labelFontSize)
        # g.set(title="{}{}{}{}{}".format(monkeys_list[m], "\n", d_prime, '\n', int(t_trial)))

        if float(HR[(HR['monkey'] == monkeys_list[m]) & (HR['task'] == '2 Visual Stimuli') &
                    (HR['stimulus'] == 'str')]['adjusted_p']) < 0.05:
            ax[m].text(0, 1.09, '*', color='black', fontsize=labelFontSize, va="top", ha="center")

        if float(HR[(HR['monkey'] == monkeys_list[m]) & (HR['task'] == '2 Visual Stimuli') &
                    (HR['stimulus'] == 'voc')]['adjusted_p']) < 0.05:
            ax[m].text(1, 1.09, '*', color='black', fontsize=labelFontSize, va="top", ha="center")

        # Plot Reaction Times
        f = sns.boxenplot(y="RT", x="stimulus", order=('str', 'voc'), showfliers=False,
                          color=palette[monkeys_list[m]],
                          data=Responses[(Responses['monkey'] == monkeys_list[m]) &
                                         (Responses['outcome'] == 'correct') &
                                         (Responses['task'] == '2 Visual Stimuli')],
                          ax=ax[m + len(monkeys_list)])

        f.set(xlabel=None, ylabel=None)
        ax[m + len(monkeys_list)].set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8])
        if m == 0:
            # f.set(ylabel='Reaction Time\n[seconds]')
            ax[m + len(monkeys_list)].set_ylabel(ylabel='Reaction Time\n[seconds]', fontsize=labelFontSize)

        ax[m + len(monkeys_list)].set_xticklabels([])
        ax[m + len(monkeys_list)].tick_params(labelsize=labelFontSize)

        a = Responses[(Responses['monkey'] == monkeys_list[m]) &
                      (Responses['outcome'] == 'correct') &
                      (Responses['stimulus'] == 'str') &
                      (Responses['task'] == '2 Visual Stimuli')]['RT']

        b = Responses[(Responses['monkey'] == monkeys_list[m]) &
                      (Responses['outcome'] == 'correct') &
                      (Responses['stimulus'] == 'voc') &
                      (Responses['task'] == '2 Visual Stimuli')]['RT']

        test, p = sps.kruskal(a, b)

        median_RT_a = a.median()
        IQR_RT_a = a.quantile(.75) - a.quantile(.25)  # 75th percentile

        median_RT_b = b.median()
        IQR_RT_b = b.quantile(.75) - b.quantile(.25)  # 75th percentile

        STATS = STATS.append({
            'monkey': monkeys_list[m],
            'test': test,
            'stimulus': 'str',
            'median': median_RT_a,
            'IQR': IQR_RT_a,
            'task': '2 Visual Stimuli',
            'n': len(a),
            'pvalue': p},
            ignore_index=True)

        STATS = STATS.append({
            'monkey': monkeys_list[m],
            'test': test,
            'stimulus': 'voc',
            'median': median_RT_b,
            'IQR': IQR_RT_b,
            'task': '2 Visual Stimuli',
            'n': len(b),
            'pvalue': p},
            ignore_index=True)

        if p < 0.05:
            ax[m + len(monkeys_list)].text(.5, 0.5, '*', color='black', fontsize=labelFontSize, va="top", ha="center")

    # Plot the 3 Visual Stimuli
    else:
        plot_df = HR[(HR['monkey'] == monkeys_list[m]) & (HR['task'] == '3 Visual Stimuli')]
        yval = plot_df[plot_df['monkey'] == monkeys_list[m]]['ignored'] + \
               plot_df[plot_df['monkey'] == monkeys_list[m]]['hits']

        # Plot bar plots
        g = sns.barplot(x='stimulus', y=yval, color='#7FFF00', order=('str', 'voc'),
                        data=plot_df[plot_df['monkey'] == monkeys_list[m]], ax=ax[m])
        g = sns.barplot(x='stimulus', y='hits', color=palette[monkeys_list[m]], order=('str', 'voc'),
                        data=plot_df[plot_df['monkey'] == monkeys_list[m]], ax=ax[m])

        g.set(ylim=[0, 1], ylabel=None, xlabel=None)

        ax[m].set_yticks([0.1, 0.3, 0.5, 0.7, 0.9])
        ax[m].tick_params(labelsize=labelFontSize)


        if m < 9:
            ax[m].axhline(0.50, color='k', linestyle='--', alpha=0.7)
        else:
            ax[m].axhline(0.33, color='k', linestyle='--', alpha=0.7)

        d_prime = float(
            dP_df[(dP_df['monkey'] == monkeys_list[m]) & (dP_df['task'] == '3 Visual Stimuli')]['dprime'])
        t_trial = float(
            dP_df[(dP_df['monkey'] == monkeys_list[m]) & (dP_df['task'] == '3 Visual Stimuli')]['trials'])

        ax[m].set_title("{}{}{}{}{}".format(monkeys_list[m], "\n", d_prime, '\n', int(t_trial)), fontsize=labelFontSize)
        # g.set(title="{}{}{}{}{}".format(monkeys_list[m], "\n", d_prime, '\n', int(t_trial)))

        if float(HR[(HR['monkey'] == monkeys_list[m]) & (HR['task'] == '3 Visual Stimuli') &
                    (HR['stimulus'] == 'str')]['adjusted_p']) < 0.05:
            ax[m].text(0, 1.09, '*', color='black', fontsize=labelFontSize, va="top", ha="center")

        if float(HR[(HR['monkey'] == monkeys_list[m]) & (HR['task'] == '3 Visual Stimuli') &
                    (HR['stimulus'] == 'voc')]['adjusted_p']) < 0.05:
            ax[m].text(1, 1.09, '*', color='black', fontsize=labelFontSize, va="top", ha="center")

        # Plot Reaction Times
        f = sns.boxenplot(y="RT", x="stimulus", order=('str', 'voc'), showfliers=False,
                          color=palette[monkeys_list[m]],
                          data=Responses[(Responses['monkey'] == monkeys_list[m]) &
                                         (Responses['outcome'] == 'correct') &
                                         (Responses['task'] == '3 Visual Stimuli')],
                          ax=ax[m + len(monkeys_list)])

        f.set(xlabel=None, ylabel=None)
        ax[m + len(monkeys_list)].set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8])
        ax[m + len(monkeys_list)].set_xticklabels([])
        ax[m + len(monkeys_list)].tick_params(labelsize=labelFontSize)

        a = Responses[(Responses['monkey'] == monkeys_list[m]) &
                      (Responses['outcome'] == 'correct') &
                      (Responses['stimulus'] == 'str') &
                      (Responses['task'] == '3 Visual Stimuli')]['RT']

        b = Responses[(Responses['monkey'] == monkeys_list[m]) &
                      (Responses['outcome'] == 'correct') &
                      (Responses['stimulus'] == 'voc') &
                      (Responses['task'] == '3 Visual Stimuli')]['RT']

        test, p = sps.kruskal(a, b)

        median_RT_a = a.median()
        IQR_RT_a = a.quantile(.75) - a.quantile(.25)  # 75th percentile

        median_RT_b = b.median()
        IQR_RT_b = b.quantile(.75) - b.quantile(.25)  # 75th percentile

        STATS = STATS.append({
            'monkey': monkeys_list[m],
            'test': test,
            'stimulus': 'str',
            'median': median_RT_a,
            'IQR': IQR_RT_a,
            'task': '3 Visual Stimuli',
            'n': len(a),
            'pvalue': p},
            ignore_index=True)

        STATS = STATS.append({
            'monkey': monkeys_list[m],
            'test': test,
            'stimulus': 'voc',
            'median': median_RT_b,
            'IQR': IQR_RT_b,
            'task': '3 Visual Stimuli',
            'n': len(b),
            'pvalue': p},
            ignore_index=True)

        if p < 0.05:
            ax[m + len(monkeys_list)].text(.5, 0.5, '*', color='black', fontsize=labelFontSize, va="top", ha="center")

ax[len(monkeys_list)].set_xticklabels(['sTr', 'voc'], rotation=90)

# save the plot
if saveplot:
    plt.savefig('./analysis_output/Figure_3CD.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_3CD.png', format='png')
    plt.close()

# Prepare the dataframes to be put in the csv and txt files
HR = HR.sort_values(['monkey', 'task']).reset_index(drop=True)

adjusted_p = multipletests(pvals=STATS['pvalue'], alpha=0.05, method="b")
STATS['adj-pvalue'] = adjusted_p[1]
STATS = STATS.rename(columns={"n": "total trials", "test": "Kruskal-Wallis"})

STATS = STATS.sort_values(['monkey', 'task', 'stimulus']).reset_index(drop=True)
dP_df = dP_df.sort_values(['monkey', 'task']).reset_index(drop=True)
HR = HR.sort_values(['monkey', 'task', 'stimulus']).reset_index(drop=True)


# save the tables
if savetable:
    STATS.to_csv(r'./analysis_output/Figure_3CD_RTs.csv', sep=';', decimal=".", index=False)
    STATS.to_csv(r'./analysis_output/Figure_3CD_RTs.txt', sep=';', decimal=".", index=False)

    HR.to_csv(r'./analysis_output/Figure_3CD_HR_binomial.csv', sep=';', decimal=".", index=False)
    HR.to_csv(r'./analysis_output/Figure_3CD_HR_binomial.txt', sep=';', decimal=".", index=False)

    dP_df.to_csv(r'./analysis_output/Figure_3CD_dPrime.csv', sep=';', decimal=".", index=False)
    dP_df.to_csv(r'./analysis_output/Figure_3CD_dPrime.txt', sep=';', decimal=".", index=False)
