# -*- coding: utf-8 -*-
"""
This script generates plots and tables related to Figure 1 of the manuscript:

"Flexible auditory training, psychophysics, and enrichment
of common marmosets with an automated, touchscreen-based system"

by Calapai A.*, Cabrera-Moreno J.*, Moser T., Jeschke M.

* shared contribution

script author: Calapai A. (acalapai@dpz.eu)

December 2021

list of output files:
- Figure_1.txt
- Figure_1_MedianTrials.txt ; Figure_1_MedianTrials.csv
- Figure_1A.txt , Figure_1A.csv
- Figure_1A.pdf , Figure_1A.png
- Figure_1B.pdf , Figure_1B.png
- Figure_1C.pdf , Figure_1C.png
- Figure_1D.pdf , Figure_1D.png

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pingouin as pg

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

result_filename = "./analysis_output/Figure_1.txt"
pd.options.mode.chained_assignment = None
# =============================================
# Parameters for the analysis
CRT_minimumTrials = 10
CRT_minimumTrials_TS = 3000

# =============================================
# Load the data for Figure 1

def dataload():
    sessions_df = pd.read_csv('./data/Figure_1.csv', low_memory=False,  decimal='.', sep=';')

    # Format the columns of the imported curated data file
    sessions_df['crashed'] = sessions_df['crashed'].astype(float)
    sessions_df['switched'] = sessions_df['switched'].astype(float)
    sessions_df['trials'] = sessions_df['trials'].astype(float)
    sessions_df['duration'] = sessions_df['duration'].astype(float)
    sessions_df['session'] = sessions_df['session'].astype(float)
    sessions_df['medianTimes'] = sessions_df['medianTimes'].astype(float)

    return sessions_df


# =============================================
# FIGURE 1A
figure1A_height = (90 / 25.4) * sizeMult
figure1A_width = (90 / 25.4) * sizeMult

# load the data
sessions_df = dataload()
plot_df = sessions_df.copy(deep=False)

# initialize variables for counting and plotting number of trials
zerotrials = []
total = []

# for each animal count the number of trials per session
for m in sessions_df['animal'].unique():
    zerotrials.append(len(sessions_df[(sessions_df['animal'] == m) & (sessions_df['trials'] == 0)]))
    total.append(len(sessions_df[(sessions_df['animal'] == m)]))

# initialize figure
f, ax = plt.subplots(2, 2, sharey='row', sharex='col',
                     gridspec_kw={'width_ratios': [len(sessions_df.animal.unique()), 1],
                                  'height_ratios': [4, 1]}, constrained_layout=True,
                     figsize=(figure1A_width, figure1A_height))

f.suptitle('Total trials per session across animals', fontsize=titleFontSize)

# plot the number of session for each animal
g = sns.barplot(x=sessions_df['animal'].unique(),
                y=total,
                ax=ax[1, 0], color="gray", edgecolor="gray")

# plot the number of session without trials for each animal
f = sns.barplot(x=sessions_df['animal'].unique(),
                y=zerotrials, ax=ax[1, 0], color="orange", edgecolor="orange")

# plot the average number of sessions across animals
mean_sessions = []
mean_sessions.append(sessions_df.groupby('animal')['session'].count().values.mean())
sns.barplot(x=None, y=mean_sessions, ax=ax[1, 1], color="grey", edgecolor="gray")
sns.barplot(x=None, y=zerotrials, ax=ax[1, 1], ci=None, color="orange", edgecolor="orange")

# plot the number of trials for each animal
sns.boxenplot(x='animal', y='trials', data=plot_df, color="grey", showfliers=False, ax=ax[0, 0])
sns.stripplot(x='animal', y='trials', data=plot_df, color="black", alpha=.1, ax=ax[0, 0])
sns.boxenplot(x=None, y='trials', data=plot_df, color="orange", showfliers=False, ax=ax[0, 1])

# aesthetics
ax[1, 0].set_yticks([0, 100, 200])
ax[0, 0].set_ylabel(ylabel='Trials', fontsize=labelFontSize)
ax[0, 0].set_xlabel(xlabel=None)
ax[0, 0].tick_params(labelsize=8)

ax[1, 0].set_ylabel(ylabel='sessions', fontsize=labelFontSize)
ax[1, 1].set_xticklabels({'All'})
ax[1, 1].text(0, np.mean(zerotrials), int(np.mean(zerotrials)),
              color='black', fontsize=8, va="bottom", ha="center")

ax[1, 0].text(13.5, 160, 'Total Sessions', color='grey', fontsize=8, va="bottom", ha="right")
ax[1, 0].text(13.5, 120, 'with 0 trials', color='orange', fontsize=8, va="bottom", ha="right")

ax[0, 1].set(ylabel=None)
ax[0, 1].text(0, int(np.median(plot_df['trials'])), int(np.median(plot_df['trials'])),
              color='black', fontsize=7, va="bottom", ha="center")

# save the figure
if saveplot:
    plt.savefig('./analysis_output/Figure_1A.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_1A.png', format='png')
    plt.close()

# save the table of the figure
if savetable:
    T = pd.DataFrame()
    T['monkey'] = sessions_df.animal.unique()
    T['trials'] = sessions_df.groupby(['animal'])['trials'].sum().values
    T['sessions'] = total
    T['zerotrials'] = zerotrials
    T.to_csv(r'./analysis_output/Figure_1A.txt', sep=';', index=False)
    T.to_csv(r'./analysis_output/Figure_1A.csv', sep=';', index=False)

# ==========================================================================================
# FIGURE 1B - Distribution of sessions duration
figure1B_height = (45 / 25.4) * sizeMult
figure1B_width = (90 / 25.4) * sizeMult

# load the data
sessions_df = dataload()
plot_df = sessions_df.copy(deep=False)
plot_df = plot_df[['device', 'date', 'duration']]

# find unique sessions across all animal groups
plot_df = plot_df.sort_values(by=['date', 'device', 'duration'])
plot_df = plot_df.drop_duplicates(subset=['device', 'date'], keep="last", inplace=False)

# initialize figure
g, ax = plt.subplots(constrained_layout=True, figsize=(figure1B_width, figure1B_height))

# plot session's duration in minutes
sns.histplot(plot_df['duration'] / 60, color="grey", bins=30, ax=ax)

# aesthetics
label = 'N = ' + str(len(plot_df))
ax.text(8.5, 145, label, color='black', fontsize=10, va="top", ha="right")
plt.xlim(0, 9)
plt.xlabel(xlabel='Hours')
plt.ylabel(ylabel='#')
plt.title('Distribution of sessions duration', y=1.0, fontsize=titleFontSize)

# save the table of the figure
if saveplot:
    plt.savefig('./analysis_output/Figure_1B.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_1B.png', format='png')
    plt.close()

# ================================================
# Statistical testing on Trials across Sessions
sessions_df = dataload()

# Make a copy of the summary dataframe (sessions_df) to summarize sessions from all experiments
partial_df = sessions_df.copy(deep=False)

# Only select animal, date, duration, trials, information to obtain information on each session
partial_df = partial_df[['animal', 'date', 'duration', 'trials', 'crashed', 'switched']]

# Sort by animal and date to consider the chronologically order of the sessions
partial_df = partial_df.sort_values(by=['animal', 'date'])

# For each animal, number the session in chronological order
partial_df['absolute_session_number'] = 0
for m in partial_df.animal.unique():
    partial_df.loc[partial_df['animal'] == m, 'absolute_session_number'] = range(1, len(
        partial_df[partial_df['animal'] == m]) + 1)

# Calculate the partial correlation between trials and absolute session number while controlling for duration
partial = pg.partial_corr(data=partial_df, x='trials', y='absolute_session_number', covar='duration')
partial_df.pcorr().round(3)

# ================================================
# Save descriptive statistics into csv and text files
if savetable:
    IQR = sessions_df.loc[:, 'trials'].quantile([.25, .5, .75]).to_list()
    with open(result_filename, "w+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        file_object.write("{} {}".format('Figure 1A: \n1st, 2nd, and 3rd quantiles of trials per session:', IQR))
        file_object.write("\n")
        file_object.write("{} {}".format('Number of total sessions: ', len(sessions_df)))
        file_object.write("\n")
        file_object.write("{} {}".format('Number of sessions without end information: ',
                                         partial_df['crashed'].sum() - partial_df['switched'].sum()))
        file_object.write("\n")
        file_object.write("{} {}".format('Percentage of sessions without end information: ',
                                         ((partial_df['crashed'].sum() - partial_df['switched'].sum()) / len(
                                             partial_df)) * 100))
        file_object.write("\n")
        file_object.write("{} {}".format('Percentage of sessions with no trials performed: ',
                                         int(len(sessions_df[sessions_df['trials'] == 0]) / len(sessions_df) * 100)))
        file_object.write("\n")
        file_object.write("{} {}".format('Quantiles of sessions no trials performed (0.25, 0.5, 0.75): ',
                                         np.quantile(np.array(zerotrials) / np.array(total), [0.25, 0.5, 0.75])))
        file_object.write("\n")
        file_object.write(
            "{} {}".format('Partial correlation trials vs sessions (controlling for duration), p-value:',
                           float(partial['p-val'])))
        file_object.write("\n")
        file_object.write(
            "{} {}".format('Partial correlation trials vs sessions (controlling for duration), adjusted r2:',
                           float(partial['r'])))
        file_object.write("\n")
        file_object.write(
            "{} {}".format('Median duration of sessions (incl crashed and switched): ',
                           int(plot_df['duration'].median())))
        file_object.write("\n")

# ===================================================================
# FIGURE 1C - Cumulative Frequency Distribution of relative trial start (all animals) with 90% mark
figure1C_height = (45 / 25.4) * sizeMult
figure1C_width = (90 / 25.4) * sizeMult

# initialize figure
f, ax = plt.subplots(figsize=(figure1C_width, figure1C_height), constrained_layout=True)

# load the data
sessions_df = dataload()
plot_df = sessions_df.copy(deep=False)

# plot the distribution of the median trial across sessions
ax.hist(plot_df[(plot_df['crashed'] == 0) & (plot_df['trials'] > 10)]['medianTimes'], color="grey", bins=30)
ax.set_xlabel('Session Proportion')
ax.set_ylabel(ylabel='#')
ax.set_xlim(0, 1)

# mark the center of the distribution
med = np.median(plot_df[(plot_df['crashed'] == 0) & (plot_df['trials'] > 10)]['medianTimes'])
label = 'N = ' + str(len(plot_df[(plot_df['crashed'] == 0) & (plot_df['trials'] > 10)]['medianTimes']))
ax.text(0.95, 40, label, color='black', fontsize=10, va="bottom", ha="right")
ax.axvline(med, color='orange', linestyle='--')
ax.set_xticks([0.25, 0.5, 0.75])
ax.set_title('Time at which 50% of trials are performed', y=1.0, fontsize=titleFontSize)

# save the plot
if saveplot:
    plt.savefig('./analysis_output/Figure_1C.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_1C.png', format='png')
    plt.close()

# save the information in the txt file initialized before
if saveplot:
    with open(result_filename, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        file_object.write("{} {}".format('Figure 1C: 50% of trials at', str(round(med, 2))))
        file_object.write("\n")

# ===============================================================
# FIGURE 1D - Distribution of relative trial start across animals
figure1D_height = (180 / 25.4) * sizeMult
figure1D_width = (90 / 25.4) * sizeMult

# load the data
sessions_df = dataload()

# extract the trial time information from each row
for i in range(len(sessions_df)):
    if str(sessions_df['times'][i]) != 'nan':
        sessions_df['times'][i] = eval(sessions_df['times'][i])
sessions_df["times"].apply(lambda x : np.array(x).flatten())

# count the total amount of trials for each animal
trial_sum = sessions_df.groupby(['animal'])['trials'].sum()
trial_sum = trial_sum[trial_sum > CRT_minimumTrials_TS]

# create a list of animals based on their total amount of trials
monkeys_list = trial_sum.index.values

# initialize the figure
fig = plt.figure(constrained_layout=True, figsize=(figure1D_width, figure1D_height))
gs = plt.GridSpec(nrows=len(monkeys_list), ncols=1, figure=fig,
                  height_ratios=[1] * len(monkeys_list), wspace=0, hspace=0)
ax = [None] * (len(monkeys_list) + 1)

# plot animals one by one, based on the order in "monkey_list"
for i in range(len(monkeys_list)):
    ax[i] = fig.add_subplot(gs[i, 0])
    label = str('Animal ' + monkeys_list[i][0:3]) + ', sessions ' + str(
        len(sessions_df[(sessions_df['animal'] == monkeys_list[i]) &
                        (sessions_df['trials'] > 10) &
                        (sessions_df['crashed'] == 0)]['times']))

    ax[i].eventplot(sessions_df[(sessions_df['animal'] == monkeys_list[i]) &
                                (sessions_df['trials'] > 10) &
                                (sessions_df['crashed'] == 0)]['times'].to_numpy(),
                    color="grey", lineoffsets=1, linelengths=1)
    ax[i].set_xlim(0, 1)
    ax[i].set_ylim(0, )
    ax[i].set_xticks([])
    ax[i].set_yticks([])
    ax[i].set_title(label, y=0.85, loc='right', fontsize=8)

    if i == len(monkeys_list) - 1:
        plt.xlabel('Session Proportion')
        ax[i].set_xticks([0.25, 0.5, 0.75])

# save the plot
if saveplot:
    plt.savefig('./analysis_output/Figure_1D.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_1D.png', format='png')
    plt.close()

# append the information in the text file opened before
with open(result_filename, "a+") as file_object:
    file_object.seek(0)
    data = file_object.read(100)
    file_object.write("{} {}".format('Figure 1D: number of animals > 3000 trials:', len(monkeys_list), monkeys_list))
    file_object.write("\n")

# compute and save additional Statistics on median amount of trials
MedianTrials = sessions_df.groupby(['animal'], as_index=False)['trials'].median()

# due to a low number of trials per session, animal n trials per sessions are computed as mean instead of median
MedianTrials['trials'][MedianTrials['animal'] == 'n'] = sum(sessions_df[sessions_df['animal'] == 'n']['trials']) / \
                                                        len(sessions_df[sessions_df['animal'] == 'n']['trials'])

# Round the average amount of trials per session
MedianTrials['trials'] = round(MedianTrials['trials'])

if savetable:
    MedianTrials.to_csv(r'./analysis_output/Figure_1_MedianTrials.csv', sep=',', index=False)
    MedianTrials.to_csv(r'./analysis_output/Figure_1_MedianTrials.txt', sep=',', index=False)
