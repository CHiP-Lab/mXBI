# Flexible auditory training, psychophysics, and enrichment of common marmosets with an automated, touchscreen-based system

**Calapai, A.\*, Cabrera-Moreno, J.\*, Moser, T., Jeschke, M.\#**

\* - contributed equally; \# - corresponding author

This document illustrates the steps required to reproduce the plots and tables on which the manuscripts' figures, statistics and tables are based. Plots that compose the figures are generated from python scripts located in the folder data_analysis. Each python script opens one or multiple curated data files contained in the folder data_analysis/data and produces multiple output files that are ultimately saved into the folder *analysis_output*. 

The estimated run time for generating all plots and tables is less than 5 minutes.

All plots are imported and processed with the software Affinity Designer 1.8.1 to create the final figure layout, improve readability of the underlying data, and fine-tune text size, colours, and position.

## How to reproduce the plots:
### Installation of required software
1. Set up a python 3.9 environment
2. Install the following modules:
   1. seaborn 0.11.1 
   2. pingouin 0.3.12
   3. psignifit 0.1 (via: `pip install https://github.com/wichmann-lab/python-psignifit/zipball/master`)

### Running of scripts to recreate each figure
3. Locate each figure script in the main folder of the repository and open it.
4. Before running each python script:
   1. Set the desired scaling factor for the plots by changing the variable `sizeMult` (1 is the size as seen in the manuscript) 
   2. Set if plots need to be saved by assigning the variable `saveplot` to 0 or 1; if 1 is selected the plots are saved but not shown at the end of the run
   3. Similarly to 2, set if tables are saved by assigning the variable `savetable` to 0 or 1. 
   Note: By default, the script will not show the plots (and corresponding tables) and instead it will save them in the folder *analysis_output*.
5. Run the scripts in any order (scripts are independent)

[![DOI](https://zenodo.org/badge/436295956.svg)](https://zenodo.org/badge/latestdoi/436295956)
