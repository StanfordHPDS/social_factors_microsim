import pandas as pd
import numpy as np
import time
from functions import *
import os

# identify overall folder directory for reading/saving files
current_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)
overall_folder = os.path.dirname(parent_directory)


def generate_transitions_HS_standard(current_state_HS, current_state_DNH):
    # Function:
    #   Returns a transition probability array for health system utilization
    #   states given the current health system utilization state
    #   and disease natural history state
    # Args:
    #   current_state_HS: current health system utilization state
    #   current_state_DNH: current disease natural history state
    # Returns:
    #   an array of health system utilization transition probabilties
    #   [out of health system (OHS),
    #   in health system (IHS),
    #   detected/treated (DT),
    #   detected/untreated (DUT)]

    transition_vec = dict()

    # if dead, stay in current state
    if current_state_DNH == "D":
        transition_vec["OHS"] = [1, 0, 0, 0]
        transition_vec["IHS"] = [0, 1, 0, 0]
        transition_vec["DT"] = [0, 0, 1, 0]
        transition_vec["DUT"] = [0, 0, 0, 1]
    # if sick, can transition to any state
    elif current_state_DNH == "S":
        transition_vec["OHS"] = [1 - pOI, pOI, 0, 0]
        transition_vec["IHS"] = [0, 1 - pDT, pDT, 0]
        transition_vec["DT"] = [0, 0, 1 - pDTUT, pDTUT]
        transition_vec["DUT"] = [0, 0, 0, 1]
    # If healthy, no transition into detected/treated
    else:
        transition_vec["OHS"] = [1 - pOI, pOI, 0, 0]
        transition_vec["IHS"] = [0, 1, 0, 0]
        transition_vec["DT"] = [0, 0, 1, 0]
        transition_vec["DUT"] = [0, 0, 0, 1]

    return transition_vec[current_state_HS]


# Read in 2021 U.S. Life tables
# Non-Hispanic Black (NHB)
male_life_table_NHB = pd.read_excel(
    f"{overall_folder}/data_and_inputs/2021_life_tables/NonHispanicBlackMale.xlsx"
)
female_life_table_NHB = pd.read_excel(
    f"{overall_folder}/data_and_inputs/2021_life_tables/NonHispanicBlackFemale.xlsx"
)
# Non-Hispanic Black (NHW)
male_life_table_NHW = pd.read_excel(
    f"{overall_folder}/data_and_inputs/2021_life_tables/NonHispanicWhiteMale.xlsx"
)
female_life_table_NHW = pd.read_excel(
    f"{overall_folder}/data_and_inputs/2021_life_tables/NonHispanicWhiteFemale.xlsx"
)

# Transform lifetables (definition in functions.py)
male_life_table_NHB = transform_lifetables(male_life_table_NHB)
female_life_table_NHB = transform_lifetables(female_life_table_NHB)
male_life_table_NHW = transform_lifetables(male_life_table_NHW)
female_life_table_NHW = transform_lifetables(female_life_table_NHW)

# Set-up mapping for life tables in functions
life_table_mapping = {
    ("NHB", "F"): female_life_table_NHB,
    ("NHB", "M"): male_life_table_NHB,
    ("NHW", "F"): female_life_table_NHW,
    ("NHW", "M"): male_life_table_NHW,
}


def generate_transitions_DNH_standard(
    current_state_HS, current_state_DNH, age, sex, race, new_treatment
):
    # Function:
    #   Returns a transition probability array for disease natural history
    #   states given the current health system utilization state,
    #   disease natural history state, age, sex, race/ethnicity, and
    #   use of new treatment
    # Args:
    #   current_state_HS: current health system utilization state
    #   current_state_DNH: current disease natural history state
    #   age: current individual's age
    #   race: current individual's race/ethnicity (either NHB or NHW)
    #   new_treatment: new treatment (True or False)
    # Returns:
    #   an array of disease natural history transition probabilties
    #   [Healthy (H),
    #   Sick (S),
    #   Dead (D)]

    # if new treatment = True, we use more effective treatment hazard ratio
    if new_treatment == True:
        rr_SD_dt = treatment_HR_NT * rr_SD_not_dt
    else:
        rr_SD_dt = treatment_HR_SC * rr_SD_not_dt

    transition_vec = dict()

    # no one survives past age 100
    if age < 100:
        life_table = life_table_mapping[(race, sex)]
        # obtain probability of death
        pHD = life_table[life_table["age"] == int(age)]["qx"].iloc[0]

        # out of the health care system
        if current_state_HS == "OHS":
            # healthy
            transition_vec["H"] = [1 - pHS - pHD, pHS, pHD]
            # increase mortality rate for sick individuals
            rHD = convert_to_prob(pHD)
            rSD_not_dt = rHD * rr_SD_not_dt
            pSD_not_dt = convert_to_prob(rSD_not_dt)
            transition_vec["S"] = [0, 1 - pSD_not_dt, pSD_not_dt]
            # Dead
            transition_vec["D"] = [0, 0, 1]

        # in the health care system
        elif current_state_HS == "IHS" or current_state_HS == "DUT":
            # increase mortality rate for sick individuals (same as
            # out of health system (OHS))
            rHD = convert_to_prob(pHD)
            rSD_not_dt = rHD * rr_SD_not_dt
            pSD_not_dt = convert_to_prob(rSD_not_dt)

            transition_vec["H"] = [1 - pHS - pHD, pHS, pHD]
            transition_vec["S"] = [0, 1 - pSD_not_dt, pSD_not_dt]
            transition_vec["D"] = [0, 0, 1]
        # detected and treated
        else:
            transition_vec["H"] = [1 - pHS - pHD, pHS, pHD]

            # increase mortality rate but include the treatment effect
            rHD = convert_to_prob(pHD)
            rSD_dt = rHD * rr_SD_dt
            pSD_dt = convert_to_prob(rSD_dt)
            transition_vec["S"] = [0, 1 - pSD_dt, pSD_dt]
            transition_vec["D"] = [0, 0, 1]
    # all individuals aged 100 progress to death
    else:
        transition_vec = dict()
        transition_vec["H"] = [0, 0, 1]
        transition_vec["S"] = [0, 0, 1]
        transition_vec["D"] = [0, 0, 1]

    # return transition vector for current disease natural history state
    return transition_vec[current_state_DNH]


def run_cohort_standard(new_treatment):
    # Function:
    #   Runs standard microsimulation model
    #   Returns health system utilization trace
    #   (pandas dataframe of each individual's health system state every year)
    #   disease natural history trace
    #   (pandas dataframe of each individual's disease natural history state every year)
    #   and combination of starting patient characteristics and the two traces
    # Args:
    #   new_treatment: new treatment (True or False)
    # Returns:
    #   HS_state_trace_df: health system utilization trace
    #   state_trace_df: disease natural history trace
    #   total_trace: combination of starting patient characteristics (population_df),
    #   and health system utilization trace (HS_state_trace_df), and
    #   disease natural history trace (state_trace_df)

    population_df = pd.read_csv(f"{overall_folder}/results/cohort.csv")
    N = len(population_df)

    # Trace to keep track of disease natural history states
    # Everyone starts healthy
    DNH_states = ["H", "S", "D"]
    initial_DNH_state = ["H" for j in range(N)]
    DNH_state_trace = np.array(
        [["ToFill" for j in range(cycles + 1)] for i in range(N)]
    )
    DNH_state_trace[:, 0] = initial_DNH_state

    # Trace to keep track of health system utilization states
    # Everyone starts in the health system
    HS_states = ["OHS", "IHS", "DT", "DUT"]
    initial_HS_state = ["IHS" for j in range(N)]
    HS_state_trace = np.array([["ToFill" for j in range(cycles + 1)] for i in range(N)])
    HS_state_trace[:, 0] = initial_HS_state

    age_values = population_df["starting_age"].tolist()

    start = time.time()
    years_to_death = [0 for i in range(N)]
    LY_disc = [0 for i in range(N)]
    death_age = [0 for i in range(N)]
    QALY_val = [0 for i in range(N)]
    QALY_disc = [0 for i in range(N)]
    COST_val = [0 for i in range(N)]
    COST_disc = [0 for i in range(N)]
    years_sick = [0 for i in range(N)]
    years_sick_treated = [0 for i in range(N)]
    years_sick_untreated = [0 for i in range(N)]
    was_sick = [0 for i in range(N)]
    was_treated = [0 for i in range(N)]

    for i in range(N):
        # each individual has their own random seed
        np.random.seed(population_df["seed"].iloc[i])
        for t in range(cycles):
            this_transition_HS = generate_transitions_HS_standard(
                HS_state_trace[i, t], DNH_state_trace[i, t]
            )
            # randomly sample next health system utilization state using
            # transition probability array
            HS_state_trace[i, t + 1] = np.random.choice(
                HS_states, size=1, p=this_transition_HS
            )[0]
            this_transition_DNH = generate_transitions_DNH_standard(
                HS_state_trace[i, t],
                DNH_state_trace[i, t],
                age_values[i],
                population_df["sex"].iloc[i],
                population_df["race"].iloc[i],
                new_treatment,
            )
            # randomly sample next disease natural history state using
            # transition probability array
            DNH_state_trace[i, t + 1] = np.random.choice(
                DNH_states, size=1, p=this_transition_DNH
            )[0]
            # age by one year
            age_values[i] = age_values[i] + 1

        # compute life years
        DNH_state_trace_LY = np.array([mapping.get(x, x) for x in DNH_state_trace[i]])
        # discounted life years
        LY_disc[i] = np.dot(DNH_state_trace_LY, v_disc)

        # compute quality-adjusted life years (QALYs)
        DNH_state_trace_QALY = np.array(
            [QALY_mapping.get(x, x) for x in DNH_state_trace[i]]
        )
        QALY_val[i] = sum(DNH_state_trace_QALY)
        # discounted QALYs
        QALY_disc[i] = np.dot(DNH_state_trace_QALY, v_disc)

        # compute costs from health states
        DNH_state_trace_COST = np.array(
            [COST_mapping.get(x, x) for x in DNH_state_trace[i]]
        )
        COST_val[i] = sum(DNH_state_trace_COST)
        # discounted costs
        COST_disc[i] = np.dot(DNH_state_trace_COST, v_disc)

        # compute additional costs from treatment
        if new_treatment:
            treatment_rows = np.where(
                (HS_state_trace[i] == "DT") & (DNH_state_trace[i] == "S"), COST_DT_NT, 0
            )
            this_treatment_COST = sum(treatment_rows)
            this_treatment_COST_disc = np.dot(treatment_rows, v_disc)
        else:
            treatment_rows = np.where(
                (HS_state_trace[i] == "DT") & (DNH_state_trace[i] == "S"), COST_DT_SC, 0
            )
            this_treatment_COST = sum(treatment_rows)
            this_treatment_COST_disc = np.dot(treatment_rows, v_disc)

        # add treatment costs to costs from health states
        COST_val[i] = COST_val[i] + this_treatment_COST
        COST_disc[i] = COST_disc[i] + this_treatment_COST_disc

        # compute death age
        years_to_death[i] = sum(DNH_state_trace_LY)
        # list(DNH_state_trace[i]).index("D")
        death_age[i] = population_df["starting_age"].iloc[i] + years_to_death[i]

        # number of years spent sick
        sick_years = np.where(DNH_state_trace[i] == "S")[0]
        years_sick[i] = len(sick_years)
        # number of years on treatment
        years_treat = np.where(HS_state_trace[i] == "DT")[0]
        overlap = [value for value in sick_years if value in years_treat]
        # number of years sick and on treatment
        years_sick_treated[i] = len(overlap)
        # number of years sick without treatment
        years_sick_untreated[i] = years_sick[i] - years_sick_treated[i]
        # cumulative incidence of sickness
        if years_sick[i] > 0:
            was_sick[i] = 1
        # cumulative incidence of detected/treated
        if len(years_treat) > 0:
            was_treated[i] = 1

    end = time.time()
    print(end - start)

    # set up columns of health system state utilization trace
    columns_trace = ["HSYear" + str(x) for x in range(0, cycles + 1)]
    HS_state_trace_df = pd.DataFrame(HS_state_trace, columns=columns_trace)
    # set up columns of disease natural history utlization trace
    columns_trace2 = ["Year" + str(x) for x in range(0, cycles + 1)]
    state_trace_df = pd.DataFrame(DNH_state_trace, columns=columns_trace2)
    # concat the starting population characteristics and two traces
    total_trace = pd.concat([population_df, state_trace_df, HS_state_trace_df], axis=1)

    # save statistics
    total_trace["years_to_death"] = pd.Series(years_to_death, index=total_trace.index)
    total_trace["discounted_LY"] = pd.Series(LY_disc, index=total_trace.index)
    total_trace["QALY"] = pd.Series(QALY_val, index=total_trace.index)
    total_trace["discounted_QALY"] = pd.Series(QALY_disc, index=total_trace.index)
    total_trace["cost"] = pd.Series(COST_val, index=total_trace.index)
    total_trace["discounted_cost"] = pd.Series(COST_disc, index=total_trace.index)
    total_trace["death_age"] = pd.Series(death_age, index=total_trace.index)
    total_trace["years_sick"] = pd.Series(years_sick, index=total_trace.index)
    total_trace["years_sick_treated"] = pd.Series(
        years_sick_treated, index=total_trace.index
    )
    total_trace["years_sick_untreated"] = pd.Series(
        years_sick_untreated, index=total_trace.index
    )
    total_trace["was_sick"] = pd.Series(was_sick, index=total_trace.index)
    total_trace["was_treated"] = pd.Series(was_treated, index=total_trace.index)

    return HS_state_trace_df, state_trace_df, total_trace
