# -*- coding: utf-8 -*-
"""
WARNING: the module "psignifit" used in this script to compute psychometric thresholds requires Python 3.6

This script generates the plots of Figure 5 (with relative summary tables) of the manuscript:
"Flexible auditory training, psychophysics, and enrichment
of common marmosets with an automated, touchscreen-based system"

by Calapai A.*, Cabrera-Moreno J.*, Moser T., Jeschke M.

* shared contribution

script author: Calapai A. (acalapai@dpz.eu)

February 2022

list of output files:
- Figure_5.txt , Figure_5.csv
- Figure_5.png , Figure_5.pdf

"""
import psignifit as ps
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =============================================
# Setting plotting parameters
sizeMult = 1
saveplot = 0
savetable = 0

labelFontSize = 6

sns.set(style="whitegrid")
sns.set_context("paper")

# =============================================
# Parameters for the analysis
CRT_minimumTrials = 100
CRT_minimumTrials_TS = 3000

pd.options.mode.chained_assignment = None
save_path = os.path.join((Path('..')).resolve(), 'analysis_output')
result_filename = os.path.join(save_path, 'Figure_5B.txt')

# =============================================
# Load the data for Figure 1

def dataload():
    AMP_df = pd.read_csv('./data/Figure_5.csv', low_memory=False, decimal=',', sep=';')
    AMP_df['total'] = AMP_df['total'].astype(float)
    AMP_df['hits'] = AMP_df['hits'].astype(float)

    return AMP_df


AMP_df = dataload()
# Manually set the color for the animals considered
cls = [[0.57, 0.47, 0.37],
       [0.50, 0.44, 0.70],
       [0.29, 0.44, 0.69]]

figure5_height = (60 / 25.4) * sizeMult
figure5_width = (140 / 25.4) * sizeMult
f, axs = plt.subplots(1, 3, sharey=True, sharex=True, gridspec_kw={'width_ratios': [1, 1, 1]},
                      constrained_layout=False, figsize=(figure5_width, figure5_height))

# Set the animals order for plotting
un_animals = ['a', 'b', 'd']

# Initialize temporary variables for the thresholds and number of trials
thrs = []
ntrs = []
CI_low = []
CI_high = []

# Cycle trough the animals
for m in range(0, len(un_animals)):
    # filter the summary dataframe into a temporary df only containing the selected animal
    subj_df = AMP_df[AMP_df.animal == un_animals[m]]
    subj_df = subj_df[["level", "hits", "total"]].to_numpy()
    subj_df = subj_df.astype(int)

    # Define properties for the psychometric fit
    options = dict()
    options['sigmoidName'] = 'norm'
    options['expType'] = 'YesNo'
    options['confP'] = [.95, .95, .95, .95]
    # options['fixedPars'] = np.nan * np.ones(5)
    # options['fixedPars'][2] = 0.01
    # options['fixedPars'][3] = 0

    # Run the fit
    res = ps.psignifit(subj_df, options)
    ps.psigniplot.plotPsych(res,
                            xLabel=None,
                            yLabel=None,
                            plotAsymptote=False,
                            fontSize=10,
                            extrapolLength=0,
                            showImediate=False,
                            dataColor=cls[m],
                            axisHandle=axs[m],
                            CIthresh=True,
                            fontName='Arial')

    # Store the results for plotting
    thrs.append(int(res['Fit'][0].round()))
    ntrs.append(sum(subj_df[:, 2]))
    CI_low.append(int(res['conf_Intervals'][0][0, 0]))
    CI_high.append(int(res['conf_Intervals'][0][1, 1]))

axs[0].set_title('Animal a', fontsize=labelFontSize)
axs[1].set_title('Animal b', fontsize=labelFontSize)
axs[2].set_title('Animal d', fontsize=labelFontSize)

axs[0].text(thrs[0] + 2, 0.05, thrs[0], fontsize=labelFontSize)
axs[1].text(thrs[1] + 2, 0.05, thrs[1], fontsize=labelFontSize)
axs[2].text(thrs[2] + 2, 0.05, thrs[2], fontsize=labelFontSize)

axs[0].text(-2, .95, "{}{}".format('N = ', ntrs[0]), fontsize=labelFontSize)
axs[1].text(-2, .95, "{}{}".format('N = ', ntrs[1]), fontsize=labelFontSize)
axs[2].text(-2, .95, "{}{}".format('N = ', ntrs[2]), fontsize=labelFontSize)

axs[0].set_ylim([0, 1])
axs[0].set_xticks([0, 15, 30, 45, 60, 75, 90])
axs[1].set_xticks([0, 15, 30, 45, 60, 75, 90])
axs[2].set_xticks([0, 15, 30, 45, 60, 75, 90])

axs[0].tick_params(labelsize=labelFontSize)
axs[1].tick_params(labelsize=labelFontSize)
axs[2].tick_params(labelsize=labelFontSize)

axs[0].set_xlabel('Amplitude (dB SPL)', fontsize=labelFontSize)
axs[0].set_ylabel('Proportion correct', fontsize=labelFontSize)

f.tight_layout()

AMP_df['groups'] = AMP_df['level'] > 50
result = AMP_df.groupby(['animal', 'level', 'groups'])['total'].sum().reset_index()
result = result.groupby(['animal', 'groups'])['total'].agg(['mean', 'std']).reset_index()
result['groups'] = result['groups'].replace({True: 'high', False: 'low'})

if saveplot:
    # Save the plot
    filename_pdf = os.path.join(save_path, 'Figure_5B.pdf')
    filename_png = os.path.join(save_path, 'Figure_5B.png')

    # Save to the main data analysis folder
    plt.savefig(filename_pdf, format='pdf')
    plt.savefig(filename_png, format='png')

    # Save also into the root folder
    plt.savefig('Figure_5.pdf', format='pdf')
    plt.savefig('Figure_5.png', format='png')
    plt.close()

# ================================================
# Save descriptive statistics into csv and text files
if savetable:

    filename_csv = os.path.join(save_path, 'Figure_5B_trials.csv')
    filename_txt = os.path.join(save_path, 'Figure_5B_trials.txt')

    result.to_csv(filename_csv, sep=',', index=False)
    result.to_csv(filename_txt, sep=',', index=False)

    with open(result_filename, "w+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        file_object.write("{} {}".format('Figure 5A: \nHearing thresholds for animal a, b, d :', thrs))
        file_object.write("\n")
        file_object.write("{} {}".format('CI thresholds (low) for animal a, b, d: ', CI_low))
        file_object.write("\n")
        file_object.write("{} {}".format('CI thresholds (high) for animal a, b, d: ', CI_high))
        file_object.write("\n")