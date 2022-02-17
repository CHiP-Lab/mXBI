# -*- coding: utf-8 -*-
"""
This script generates plots and tables related to Supplementary Figure 2 of the manuscript:

"Flexible auditory training, psychophysics, and enrichment
of common marmosets with an automated, touchscreen-based system"

by Calapai A.*, Cabrera-Moreno J.*, Moser T., Jeschke M.

* shared contribution

script author: Calapai A. (acalapai@dpz.eu)

February 2022

list of input files:
- Figure_S2BD_data
- Figure_S2C_data.csv

list of output files:
- Figure_S2C.pdf , Figure_S2C.png
- Figure_S2CBD.pdf , Figure_S2BD.png

"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns


# =============================================
# Setting plotting parameters
sizeMult = 1
saveplot = 1  # 1 or 0; 1 saves plots in the folder "./analysis_output" without showing them; 0 shows without plotting

tickFontSize = 8
labelFontSize = 10
titleFontSize = 10

sns.set(style="whitegrid")
sns.set_context("paper")

# =============================================
# Load the data for Figure S2C & S2BD
df_BD = pd.read_csv(r'./data/Figure_S2BD_data.csv')
df_C = pd.read_csv(r'./data/Figure_S2C_data.csv')

# =============================================
# Plot Figure S2C    
sns.lineplot(x='ntrial',y='step',data=df_C, palette="Blues")
plt.title('Progression through the steps')

if saveplot:
    plt.savefig('./analysis_output/Figure_S2C.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_S2C.png', format='png')
    plt.close()


# =============================================
# Plot Figure S2BD
p_val = 0.01
hStep = 62
grouping = 'session'
targetToPlot = ['voc','sTr','cTr']
colorBars = ['tab:blue','tab:orange','tab:green']
animalName = df_BD['animal'].unique()
  
fig = plt.figure()
figGrid = gridspec.GridSpec(ncols = 1, nrows = 4, figure = fig)

ax1 = fig.add_subplot(figGrid[0:2,:]) # HR      
ax2 = fig.add_subplot(figGrid[2,:]) # Number of trials

groupDF = df_BD.sort_values(by=[grouping]).reset_index()

# plots HR per stimulus
colsToPlot = ['animal']
[colsToPlot.append(colName) if any(x in colName for x in ['HR']) else 0 for colName in list(groupDF.columns)]
groupDF[colsToPlot].plot(ax=ax1, marker='.')

ax1.set_ylim([-5, 115])
ax1.set_title(animalName)
ax1.get_xlim()
ax1.set_xticklabels('')
ax1.grid(True)

# indicate significance and highest step
idxSig = groupDF.index[groupDF['pVal'] < p_val]
stepSig = groupDF.index[groupDF['maxStep'] >= hStep]
ax1.plot(idxSig, [105]*len(idxSig), marker='*', color = 'k', linestyle='none')
ax1.plot(stepSig, [110]*len(stepSig), marker='.', color = 'grey', linestyle='none')
ax1.set_ylabel('response rates')   


# show number of trials per session as ratio of each trial type
totalTrials = df_BD['trials']
trialsCTR = df_BD['cTr'] / totalTrials
trialsSTR = df_BD['sTr'] / totalTrials
trialsVOC = df_BD['voc'] / totalTrials
bar1 = trialsCTR+trialsSTR+trialsVOC
bar2 = trialsCTR+trialsSTR
bar3 = trialsCTR
bars = (bar1, bar2, bar3)

for index, z in enumerate(bars):
    ax2.bar(x=list(range(1,len(groupDF)+1)), height=z, color=colorBars[index])
    
# shows session, step, trials in session
for i in range(len(groupDF)):
    ax2.text(x=i+.9, y=-.50, s=int(groupDF['trials'][i]), size=10)
    ax2.text(x=i+.9, y=-.30, s=int(groupDF['session'][i]), size=10) 
    ax2.text(x=i+.9, y=-.40, s=int(groupDF['maxStep'][i]), size=10)

ax2.set_xticks([])
ax2.set_xlabel(grouping+'; step; trials', fontsize=12)
ax2.legend()
ax2.set_ylabel('%')                                       

# place legends ouside plots
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 16})
ax2.get_legend().remove()

# set title
ax1.title.set_text('Correct trials across stimulus type')
ax2.title.set_text('Proportion of stimulus type across consecutive sessions')

# set size of figure
plt.gcf().set_size_inches(16.4 , 9.34)

if saveplot:
    plt.savefig('./analysis_output/Figure_S2BD.pdf', format='pdf')
    plt.savefig('./analysis_output/Figure_S2BD.png', format='png')
    plt.close()


    
