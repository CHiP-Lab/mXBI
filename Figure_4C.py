# -*- coding: utf-8 -*-
"""
This script generates plots and tables related to Figure 4 of the manuscript:

"Flexible auditory training, psychophysics, and enrichment
of common marmosets with an automated, touchscreen-based system"

by Calapai A.*, Cabrera-Moreno J.*, Moser T., Jeschke M.

* shared contribution

script author: Calapai A. (acalapai@dpz.eu)

February 2022

list of input files:
- Animals_metaData.csv
- Figure_4C_dPDF.csv
- Figure_4C_HR.csv
- Figure_4C_Responses.csv

list of output files:
- Figure_4C_dPrime.txt, Figure_4C_dPrime.csv
- Figure_4C_HR_binomial.txt, Figure_4C_HR_binomial.csv
- Figure_4C1.pdf, Figure_4C1.png
- Figure_4C2.pdf, Figure_4C2.png
- Figure_4C3.pdf, Figure_4C3.png
- Figure_4C4.pdf, Figure_4C4.png

"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
CRT_minimumTrials = 50
CRT_minimumTrials_TS = 3000
CTRL_lastNsessions = 3
sliding_window_size = 300
bins_size = 100

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
# Load the data for Figure 3

def dataload_dpDF():
    dP_df = pd.read_csv('./data/Figure_4C_dPDF.csv', low_memory=False, sep=';', decimal='.')

    # Format the columns of the imported curated data file
    dP_df['dprime'] = dP_df['dprime'].astype(float)

    return dP_df


def dataload_HR():
    HR = pd.read_csv('./data/Figure_4C_HR.csv', low_memory=False, sep=';', decimal='.')

    # Format the columns of the imported curated data file
    HR['binomial'] = HR['binomial'].astype(float)
    HR['hits'] = HR['hits'].astype(float)
    HR['ignored'] = HR['ignored'].astype(float)
    HR['adjusted_p'] = HR['adjusted_p'].astype(float)

    return HR


def dataload_Responses():
    Responses = pd.read_csv('./data/Figure_4C_Responses.csv', low_memory=False, sep=';', decimal='.')

    # Format the columns of the imported curated data file
    Responses['RT'] = Responses['RT'].astype(float)

    return Responses


# =============================================
# Figure 4C
figure4C_height = (40 / 25.4) * sizeMult
figure4C_width = (80 / 25.4) * sizeMult

# load the data
dP_df = dataload_dpDF()
HR = dataload_HR()
Responses = dataload_Responses()

# Initialize a summary dataframe for the statistics
STATS = pd.DataFrame(columns=['monkey', 'n', 'test', 'pvalue'])

# Create stimuli and tasks dictionaries
stimuli_dict = {'voc': 'voc', 'vocMAT': 'twi', 'vocMAP': 'phee', 'str': 'str', 'wNoise': 'wNoi.'}
tasks_list = ["['infant','twitter']", "['phee','puretone']", "['twitter','puretone']", "['wnoise','twitter']"]
task_dict = {"['infant','twitter']": 'Juvenile vs Twitter',
             "['phee','puretone']": 'Phee vs Pure Tone',
             "['twitter','puretone']": 'Twitter vs Pure Tone',
             "['wnoise','twitter']": 'Noise vs Twitter'}

# Manually define a list of all possibile stimuli across tasks
all_targets = [['vocMAT', 'voc'], ['vocMAP', 'str'], ['vocMAT', 'str'], ['wNoise', 'vocMAT']]

all_rewards = [['vocMAT_reward', 'voc_reward'], ['vocMAP_reward', 'str_reward'], ['vocMAT_reward', 'str_reward'],
               ['wNoise_reward', 'vocMAT_reward']]

all_wrongs = [['vocMAT_wrong', 'voc_wrong'], ['vocMAP_wrong', 'str_wrong'], ['vocMAT_wrong', 'str_wrong'],
              ['wNoise_wrong', 'vocMAT_wrong']]

# Cycle through all tasks
for t in range(0, len(tasks_list)):
    # Close previous plot in the loop
    if saveplot:
        plt.close()

    # Initialize a figure for each task
    monkeys_list = sorted(dP_df[dP_df['task'] == tasks_list[t]]['monkey'].unique())
    g, ax = plt.subplots(1, len(monkeys_list), sharey=True, sharex=True, constrained_layout=True,
                         figsize=(figure4C_width, figure4C_height))

    ax = ax.flatten()

    # Identify the stimuli name for the current task
    stimuli = all_targets[list(tasks_list).index(tasks_list[t])]

    # Cycle through the animals of the current task
    for m in range(0, len(monkeys_list)):

        # Initialize the dataframe for the data to plot
        plot_df = HR[(HR['monkey'] == monkeys_list[m]) & (HR['task'] == tasks_list[t])]
        yval = plot_df[plot_df['monkey'] == monkeys_list[m]]['ignored'] + \
               plot_df[plot_df['monkey'] == monkeys_list[m]]['hits']

        g = sns.barplot(x='stimulus', y=yval, color='#7FFF00', order=(stimuli[0], stimuli[1]),
                        data=plot_df[plot_df['monkey'] == monkeys_list[m]], ax=ax[m])
        g = sns.barplot(x='stimulus', y='hits', color=palette[monkeys_list[m]], order=(stimuli[0], stimuli[1]),
                        data=plot_df[plot_df['monkey'] == monkeys_list[m]], ax=ax[m])

        g.set(ylim=[0, 1], ylabel=None, xlabel=None)

        ax[m].set_xticklabels([], rotation=90)
        ax[m].set_yticks([0.25, 0.5, 0.75])
        ax[m].axhline(0.50, color='k', linestyle='--', alpha=0.7)
        ax[m].tick_params(labelsize=labelFontSize)

        if m == 0:
            # g.set(ylabel='Hit rate')
            ax[m].set_ylabel(ylabel='Hit Rate', fontsize=labelFontSize)

        d_prime = float(dP_df[(dP_df['monkey'] == monkeys_list[m]) & (dP_df['task'] == tasks_list[t])]['dprime'])
        t_trial = int(sum(HR[(HR['monkey'] == monkeys_list[m]) & (HR['task'] == tasks_list[t])]['N']))
        #t_trial = float(dP_df[(dP_df['monkey'] == monkeys_list[m]) & (dP_df['task'] == tasks_list[t])]['trials'])

        ax[m].set_title("{}{}{}{}{}".format(monkeys_list[m], "\n", d_prime, '\n', int(t_trial)), fontsize=labelFontSize)
        # g.set(title="{}{}{}".format(d_prime, '\n', int(t_trial)))

        if float(HR[(HR['monkey'] == monkeys_list[m]) &
                    (HR['task'] == tasks_list[t]) &
                    (HR['stimulus'] == stimuli[0])]['adjusted_p']) < 0.05:
            ax[m].text(0, 1.09, '*', color='black', fontsize=12, va="top", ha="center")

        if float(HR[(HR['monkey'] == monkeys_list[m]) &
                    (HR['task'] == tasks_list[t]) &
                    (HR['stimulus'] == stimuli[1])]['adjusted_p']) < 0.05:
            ax[m].text(1, 1.09, '*', color='black', fontsize=12, va="top", ha="center")

        ax[len(monkeys_list) - 1].set_xticklabels([stimuli_dict[stimuli[0]], stimuli_dict[stimuli[1]]], rotation=90)

        if saveplot:
            plt.savefig('./analysis_output/Figure_4C' + str(t + 1) + '.pdf', format='pdf')
            plt.savefig('./analysis_output/Figure_4C' + str(t + 1) + '.png', format='png')

# Format the summary and statistical dataframes before saving them to files
dP_df = dP_df.sort_values(['monkey']).reset_index(drop=True)
HR = HR.sort_values(['monkey', 'stimulus']).reset_index(drop=True)
HR['condition'] = HR['task'].map(task_dict)
HR['stimulus'] = HR['stimulus'].map(stimuli_dict)

# save tables
if savetable:
    dP_df.to_csv(r'./analysis_output/Figure_4C_dPrime.csv', sep=';', decimal=".", index=False)
    dP_df.to_csv(r'./analysis_output/Figure_4C_dPrime.txt', sep=';', decimal=".", index=False)

    HR.to_csv(r'./analysis_output/Figure_4C_HR_binomial.csv', sep=';', decimal=".", index=False)
    HR.to_csv(r'./analysis_output/Figure_4C_HR_binomial.txt', sep=';', decimal=".", index=False)
