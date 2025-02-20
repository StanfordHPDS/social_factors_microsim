# A novel decision modeling framework for health policy analyses when outcomes are influenced by social and disease processes

This repository contains code for the paper "A novel decision modeling framework for health policy analyses when outcomes are influenced by social and disease processes" by Marika Cusick, Fernando Alarid-Escudero, Jeremy Goldhaber-Fiebert, and Sherri Rose.

We developed a novel decision-analytic modeling framework, social factors framework, to integrate social process into health policy simulation models. To demonstrate the value of our framework, we compared model results with and without our social factors framework for a simplified decision problem.

## Set up virtual python environment

Run the following commands to set up the virtual conda environment with the necessary packages.

```{python}
CONDA_CHANNEL_PRIORITY=flexible
conda env create -f environment.yml
conda activate sff-env
```

## Code

### Main results

The following commands run our main results and outputs into the [Results](https://github.com/StanfordHPDS/microsim-DNH-HS/tree/main/Results) folder. The `develop_cohort.py -n "cohort_size"` script creates our cohort of 100,000 individuals. The `run_model.py` runs the standard model and standard model with our social factor framework under both the standard of care and the new treatment.

```{python}
python code/python/develop_cohort.py -n "100000" 
python code/python/run_model.py
```

## Quarto

The quarto document [manuscript_draft.qmd](https://github.com/StanfordHPDS/microsim-DNH-HS/blob/main/manuscript_draft.qmd) contains the latest draft of our working paper and up-to-date results.