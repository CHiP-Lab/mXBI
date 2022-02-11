# Flexible auditory training, psychophysics, and enrichment of common marmosets with an automated, touchscreen-based system

**Calapai, A.\*, Cabrera-Moreno, J.\*, Moser, T., Jeschke, M.\#**

\* - contributed equally; \# - corresponding author

This document illustrates the steps required to reproduce the plots and tables on which the manuscripts' figures, statistics and tables are based. Plots that compose the figures are generated from python scripts located in the folder data_analysis. Each python script opens one or multiple curated data files contained in the folder data_analysis/data and produces multiple output files that are ultimately saved into the folder data_analysis/analysis_output. 

The script and curated data to produce Figure 5, which requires an earlier python version than the rest of the analysis, are located in a different folder, called data_analysis_thresholdExperiment_Figure5. The plots for Figure 5 are not saved inside this folder but in the folder data_analysis/analysis_output together with the output files of all other scripts.

The estimated run time for generating all plots and tables is 15 minutes.

All plots are imported and processed with the software Affinity Designer 1.8.1 to create the final figure layout, improve readability of the underlying data, and fine-tuning text size, colours, and position.

## How to reproduce the plots:
### Installation of required software
1. Set up a python 3.9 environment (Figure 5, in a separate folder, requires python 3.6)

2. Install the following modules:
   1. seaborn 0.11.1 
   2. pingouin 0.3.12
   3. psignifit 0.1 (only for Figure 5 and in a separate python environment)

   Note: other used modules, native to python 3.9 (e.g. string), are not listed.

### Running of scripts to recreate each figure

3. Locate each figure script in the main folder of the repository and open it.

4. Before running each python script:
   1. Set the desired scaling factor for the plots (1 is the size as seen in the manuscript) by changing the variable sizeMult

   2. Set if plots need to be saved by assigning the variable saveplot to 0 or 1; if 1 is selected, the plots are saved but not shown at the end of the run

   3. Set if tables are saved by assigning the variable savetable to 0 or 1. 

   Note: By default, the script will not show the plots and instead save them (with corresponding tables in the folder data_analysis/analysis_output.

5. Run the scripts in any order (scripts are independent)
