# -*- coding: utf-8 -*-
"""
This script generates plots and tables related to Supplementary Figure 1 of the manuscript:

"Flexible auditory training, psychophysics, and enrichment
of common marmosets with an automated, touchscreen-based system"

by Calapai A.*, Cabrera-Moreno J.*, Moser T., Jeschke M.

* shared contribution

script author: Calapai A. (acalapai@dpz.eu)

February 2022

list of output files:
- Figure_S1B_dPrime.txt, Figure_S1B_dPrime.csv
- Figure_S1B_HR_binomial.txt, Figure_S1B_HR_binomial.csv
- Figure_S1B_RTs.txt, Figure_S1B_RTs.csv
- Figure_S1A.pdf , Figure_S1A.png
- Figure_S1B.pdf , Figure_S1B.png

"""

import pandas as pd
import seaborn as sns
import scipy.stats as sps
import matplotlib.pyplot as plt
from statsmodels.stats.multitest import multipletests

# =============================================
# Setting plotting parameters
sizeMult = 1
saveplot = 1  # 1 or 0; 1 saves plots in the folder "./analysis_output" without showing them; 0 shows without plotting
savetable = 1  # 1 or 0; 1 saves tables in "./analysis_output" without showing them

# =============================================
# Parameters for the analysis
CRT_minimumTrials = 200
CRT_minimumTrials_TS = 3000
CTRL_lastNsessions = 10

CTRL_RT_min = 0.4  # in milliseconds
CTRL_RT_max = 5  # in milliseconds

sliding_window_size = 100  # in trials
bin_size = 5

tickFontSize = 8
labelFontSize = 10
titleFontSize = 10

sns.set(style="whitegrid")
sns.set_context("paper")

pd.options.mode.chained_assignment = None

monkeys_list = ['a', 'b', 'g', 'h']

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
# Load the data for Figure 4A and 4B

def dataload():
    dP_df = pd.read_csv('./data/Figure_S1_dPDF.csv', low_memory=False, sep=';', decimal=',')
    HR = pd.read_csv('./data/Figure_S1_HR.csv', low_memory=False, sep=';', decimal=',')
    DATA_filtered = pd.read_csv('./data/Figure_S1_data.csv', low_memory=False, sep=';', decimal=',')
    ABS = pd.read_csv('./data/Figure_S1_ABS.csv', low_memory=False, sep=';', decimal=',')
    plot_df = pd.read_csv('./data/Figure_S1_plot.csv', low_memory=False, sep=';', decimal=',')

    plot_df['HitRate'] = plot_df['HitRate'].astype(float)
    plot_df['p_trials'] = plot_df['p_trials'].astype(int)
    plot_df['Trials'] = plot_df['Trials'].astype(int)

    HR['hits'] = HR['hits'].astype(float)
    HR['ignored'] = HR['ignored'].astype(float)
    HR['wrong'] = HR['wrong'].astype(float)

    DATA_filtered['reactionTime'] = DATA_filtered['reactionTime'].astype(float)

    ABS['count'] = ABS['count'].astype(float)

    return dP_df, HR, DATA_filtered, ABS, plot_df


# ========================================================
# Figure S2A: plot hit rate across acoustic discrimination tasks
dP_df, HR, DATA_filtered, ABS, plot_df = dataload()

figureS2A_height = (90 / 25.4) * sizeMult
figureS2A_width = (90 / 25.4) * sizeMult

sizes = [min(plot_df.Trials.values), max(plot_df.Trials.values)]
size_thick = (2, 5)

g = plt.figure(figsize=(figureS2A_width, figureS2A_height), constrained_layout=True)
ax = sns.lineplot(x="p_trials", y="HitRate", size='Trials', hue="monkey",
                  sizes=size_thick, data=plot_df, palette=palette)

ax.set_title('Experiment 2: Artificial Discrimination', fontsize=12)
ax.set(ylabel='Hit Rate', xlabel='Percentage of Trials')
ax.set(ylim=[0, 1], xlim=[0, 100])
ax.set_yticks([0, 0.25, 0.50, 0.75, 1])
ax.axhline(0.5, color='grey', linestyle='--')
ax.legend(ncol=2, loc='lower center')

if saveplot:
    plt.savefig('./analysis_output/Figure_S1A.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_S1A.png', format='png')
    plt.close()

# ==================================================================================================================
figureS2B_height = (90 / 25.4) * sizeMult
figureS2B_width = (90 / 25.4) * sizeMult
STATS = pd.DataFrame(columns=['monkey', 'n', 'test', 'pvalue'])

g, ax = plt.subplots(2, len(monkeys_list), sharey='row', sharex='col', constrained_layout=True,
                     gridspec_kw={'height_ratios': [1, 2]}, figsize=(figureS2B_width, figureS2B_height))
g.suptitle('Performance in the last 5 sessions', fontsize=12)

ax = ax.flatten()

for m in range(0, len(monkeys_list)):
    temp_df = HR[(HR['monkey'] == monkeys_list[m]) & (HR['task'] == 'Artificial Discrimination')]
    yval = temp_df[temp_df['monkey'] == monkeys_list[m]]['ignored'] + temp_df[temp_df['monkey'] == monkeys_list[m]][
        'hits']
    g = sns.barplot(x='stimulus', y=yval, color='#7FFF00', order=('sTr', 'cTr'),
                    data=temp_df[temp_df['monkey'] == monkeys_list[m]], ax=ax[m])
    g = sns.barplot(x='stimulus', y='hits', color=palette[monkeys_list[m]], order=('sTr', 'cTr'),
                    data=temp_df[temp_df['monkey'] == monkeys_list[m]], ax=ax[m])

    g.set(ylim=[0, 1], ylabel=None, xlabel=None)

    ax[m].set_yticks([0.25, 0.5, 0.75])
    ax[m].axhline(0.50, color='k', linestyle='--', alpha=0.7)

    if m == 0:
        g.set(ylabel='Hit rate')

    d_prime = float(
        dP_df[(dP_df['monkey'] == monkeys_list[m]) & (dP_df['task'] == 'Artificial Discrimination')]['dprime'])
    t_trial = float(
        dP_df[(dP_df['monkey'] == monkeys_list[m]) & (dP_df['task'] == 'Artificial Discrimination')]['trials'])

    g.set(title="{}{}{}{}{}".format(monkeys_list[m], "\nd' = ", d_prime, '\n n = ', int(t_trial)))

    # Reaction Times
    f = sns.boxenplot(y="reactionTime", x="stimulus", order=('str', 'ctr'), showfliers=False,
                      color=palette[monkeys_list[m]],
                      data=DATA_filtered[(DATA_filtered['monkey'] == monkeys_list[m]) &
                                         (DATA_filtered['outcome'] == 'correct') &
                                         (DATA_filtered['task'] == 'Artificial Discrimination')],
                      ax=ax[m + len(monkeys_list)])

    f.set(ylim=[0, 5], xlabel=None, ylabel=None)
    ax[m + len(monkeys_list)].set_yticks([0, 1, 2, 3, 4, 5])
    if m == 0:
        f.set(ylabel='Reaction Time\n[seconds]')

    ax[m + len(monkeys_list)].set_xticklabels([])

    a = DATA_filtered[(DATA_filtered['monkey'] == monkeys_list[m]) &
                      (DATA_filtered['outcome'] == 'correct') &
                      (DATA_filtered['stimulus'] == 'str') &
                      (DATA_filtered['task'] == 'Artificial Discrimination')]['reactionTime']

    b = DATA_filtered[(DATA_filtered['monkey'] == monkeys_list[m]) &
                      (DATA_filtered['outcome'] == 'correct') &
                      (DATA_filtered['stimulus'] == 'ctr') &
                      (DATA_filtered['task'] == 'Artificial Discrimination')]['reactionTime']

    test, p = sps.kruskal(a, b)

     STATS = STATS.append({
        'monkey': monkeys_list[m],
        'test': test,
        'task': 'Artificial Discrimination',
        'stimulus': 'str',
        'n': len(a),
        'pvalue': p},
        ignore_index=True)

    STATS = STATS.append({
        'monkey': monkeys_list[m],
        'test': test,
        'task': 'Artificial Discrimination',
        'stimulus': 'ctr',
        'n': len(b),
        'pvalue': p},
        ignore_index=True)

    if p < 0.05:
        # f.legend({'*'}, loc='upper center', fontsize=20, frameon=False, title=None, handlelength=0)
        ax[m + len(monkeys_list)].text(.5, 0.5, '*', color='black', fontsize=20, va="top", ha="center")

    ax[len(monkeys_list)].set_xticklabels(['sTr', 'cTr'])

if saveplot:
    plt.savefig('./analysis_output/Figure_S1B.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_S1B.png', format='png')
    plt.close()

# Prepare the dataframes to be put in the csv and txt files
HR = HR.sort_values(['monkey', 'task']).reset_index(drop=True)

adjusted_p = multipletests(pvals=STATS['pvalue'], alpha=0.05, method="b")
STATS['adj-pvalue'] = adjusted_p[1]

STATS = STATS.sort_values(['monkey', 'task']).reset_index(drop=True)
dP_df = dP_df.sort_values(['monkey', 'task']).reset_index(drop=True)

STATS = STATS.rename(columns={"n": "total trials", "test": "Kruskal-Wallis"})

if savetable:
    STATS.to_csv(r'./analysis_output/Figure_S1B_RTs.csv', sep=';', decimal=".", index=False)
    STATS.to_csv(r'./analysis_output/Figure_S1B_RTs.txt', sep=';', decimal=".", index=False)

    HR.to_csv(r'./analysis_output/Figure_S1B_HR_binomial.csv', sep=';', decimal=".", index=False)
    HR.to_csv(r'./analysis_output/Figure_S1B_HR_binomial.txt', sep=';', decimal=".", index=False)

    dP_df.to_csv(r'./analysis_output/Figure_S1B_dPrime.csv', sep=';', decimal=".", index=False)
    dP_df.to_csv(r'./analysis_output/Figure_S1B_dPrime.txt', sep=';', decimal=".", index=False)
