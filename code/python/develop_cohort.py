import numpy as np
import pandas as pd
import json
from argparse import ArgumentParser
import os
from functions import *


parser = ArgumentParser()
parser.add_argument("-n", dest="cohort_size", required=True, help="cohort size")

args = parser.parse_args()
cohort_size = int(args.cohort_size)

# identify overall folder directory for reading/saving files
current_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)
overall_folder = os.path.dirname(parent_directory)


def develop_cohort(cohort_size):
    # Function:
    #   Generates a simulated cohort of individuals given a cohort size.
    #   The demographic and health system utilization characteristics
    #   of the simulated cohort are estimated from NHANES 2013-2018
    #   survey data (NHANES_parameter_inputs.qmd file)
    # Args:
    #   cohort_size: cohort size (e.g., "100000")
    # Returns:
    #   pandas dataframe of simulated cohort

    # set master random seed
    np.random.seed(1234)
    N = cohort_size  # number of individuals

    # get a random seed for every individual
    random_seeds = np.random.randint(1, 1000000, size=N)

    age_values = [starting_age for x in range(N)]

    # race/ethnicity is either Non-Hispanic Black (NHB) or Non-Hipsanic white (NHW)
    race_choices = ["NHB", "NHW"]
    with open(
        f"{overall_folder}/data_and_inputs/nhanes_inputs/prop_black.json", "r"
    ) as f:
        black_prop = json.load(f)[0]
    race_values = np.random.choice(race_choices, size=N, p=[black_prop, 1 - black_prop])
    # sex is either female (F) or male (M)
    with open(
        f"{overall_folder}/data_and_inputs/nhanes_inputs/prop_female.json", "r"
    ) as f:
        female_prop = json.load(f)[0]
    sex_choices = ["F", "M"]
    sex_values = np.random.choice(sex_choices, size=N, p=[female_prop, 1 - female_prop])

    # insurance is either yes (Y) or no (N)
    insurance_values = ["Y" for x in range(N)]
    with open(
        f"{overall_folder}/data_and_inputs/nhanes_inputs/insurance_prop_NHW.json", "r"
    ) as f:
        NHW_insured_prop = json.load(f)[0]
    with open(
        f"{overall_folder}/data_and_inputs/nhanes_inputs/insurance_prop_NHB.json", "r"
    ) as f:
        NHB_insured_prop = json.load(f)[0]
    # differential insurance rates applied by race/ethnicity
    insured_probs = np.where(
        np.array(race_values) == "NHB", NHB_insured_prop, NHW_insured_prop
    )
    random_draws = np.random.rand(len(insured_probs))
    insurance_values = np.where(random_draws < insured_probs, "Y", "N")

    # healthcare system utilization is either out of the health system (OHS)
    # with no routine place for care or in the health system (IHS) with routine
    # place for care
    with open(
        f"{overall_folder}/data_and_inputs/nhanes_inputs/place_prop_uninsured.json", "r"
    ) as f:
        place_uninsured_prop = json.load(f)[0]
    with open(
        f"{overall_folder}/data_and_inputs/nhanes_inputs/place_prop_insured.json", "r"
    ) as f:
        place_insured_prop = json.load(f)[0]
    # differential rates of place for care applied by insurance status
    initial_HS_state = ["OHS" for j in range(N)]
    place_probs = np.where(
        np.array(insurance_values) == "Y", place_insured_prop, place_uninsured_prop
    )
    random_draws = np.random.rand(len(insured_probs))
    initial_HS_state = np.where(random_draws < place_probs, "IHS", "OHS")

    # define the columns in the cohort dataframe
    population_df = pd.DataFrame(list(range(0, N)), columns=["id"])
    population_df["seed"] = pd.Series(random_seeds)
    population_df["starting_age"] = pd.Series(age_values)
    population_df["race"] = pd.Series(race_values)
    population_df["sex"] = pd.Series(sex_values)
    population_df["insurance"] = pd.Series(insurance_values)
    population_df["place"] = pd.Series(initial_HS_state)

    return population_df


cohort = develop_cohort(cohort_size)


# export cohort dataframe into results folder
if not os.path.exists(f"{overall_folder}/results/"):
    os.makedirs(f"{overall_folder}/results/")
cohort.to_csv(f"{overall_folder}/results/cohort.csv", index=False)
