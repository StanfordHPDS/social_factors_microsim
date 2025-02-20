import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def transform_lifetables(life_table):
    # Function:
    #   Transforms U.S. life tables by removing white space and adding an integer age column
    # Args:
    #   life_table: U.S. life table file in pandas dataframe format
    # Returns:
    #   transformed life table

    life_table = life_table[:101]
    life_table = life_table.reset_index()
    life_table = life_table.drop(columns=["index"])
    life_table["age"] = pd.Series(list(range(0, 101)), index=life_table.index)
    return life_table


def add_insurance_mortality(lifetable, p_r):
    # Function:
    #   Adjusts life table mortality rates by insurance status using
    #   a constant race/ethnicity-specific prevalence of uninsured individuals
    #   and a hazard ratio for increased mortality risk among those uninsured
    # Args:
    #   life_table: U.S. life table file in pandas dataframe format
    #   p_r: race/ethnicity-specific prevalence of uninsured individuals
    # Returns:
    #   life table with two new columns:
    #       'qx_ins' (mortality rate of insured individuals)
    #       'qx_no_ins' (mortality rate of uninsured individuals)

    insured_probs = [0 for i in range(len(lifetable))]
    notinsured_probs = [0 for i in range(len(lifetable))]
    for i in range(len(lifetable)):
        if lifetable["age"].iloc[i] != 100:
            this_rate = convert_to_rate(lifetable["qx"].iloc[i])
            insured_probs[i] = convert_to_prob(
                this_rate / (p_r + HAZARD_RATIO * (1 - p_r))
            )
            notinsured_probs[i] = convert_to_prob(
                convert_to_rate(insured_probs[i]) * HAZARD_RATIO
            )
        else:
            insured_probs[i] = 1
            notinsured_probs[i] = 1
    lifetable["qx_ins"] = pd.Series(insured_probs, index=lifetable.index)
    lifetable["qx_no_ins"] = pd.Series(notinsured_probs, index=lifetable.index)
    return lifetable


def convert_to_rate(prob):
    # Function:
    #   Coverts probabilities into rates
    # Args:
    #   prob: probability
    # Returns:
    #   rate
    return -np.log(1 - prob)


def convert_to_prob(rate):
    # Function:
    #   Coverts rates into probabilities
    # Args:
    #   prob: rates
    # Returns:
    #   probability
    return 1 - np.exp(-rate)


def run_DNS_state_graph(trace, plot=False):
    # Function:
    #   Creates arrays with the proportion of individuals who are in each of the disease natural
    #   history states: healthy (H), sick (S), and dead (D)
    #   Plots the arrays as a function of age
    # Args:
    #   trace: disease natural history trace
    #   plot: if True, plots the figure
    # Returns:
    #   H_arr: proportion of individuals who are in the healthy state
    #   S_arr: proportion of individuals who are in the sick state
    #   D_arr: proportion of individuals who are in the dead state
    #   If plot = True, plots H_arr, S_arr, D_arr as a function of age

    N = len(trace)
    H_arr = []
    S_arr = []
    D_arr = []
    for i in trace.columns:
        H_arr.append(len(np.where(trace[i] == "H")[0]) / N)
        S_arr.append(len(np.where(trace[i] == "S")[0]) / N)
        D_arr.append(len(np.where(trace[i] == "D")[0]) / N)
    if plot == True:
        plt.figure(figsize=(8, 5))
        plt.plot(
            range(starting_age + 0, starting_age + cycles + 1), H_arr, label="Healthy"
        )
        plt.plot(
            range(starting_age + 0, starting_age + cycles + 1), S_arr, label="Sick"
        )
        plt.plot(
            range(starting_age + 0, starting_age + cycles + 1), D_arr, label="Dead"
        )
        plt.legend()
        plt.ylabel("State proportion")
        plt.xlabel("Age")
    return H_arr, S_arr, D_arr


def run_HS_state_graph(trace, plot=False):
    # Function:
    #   Creates arrays with the proportion of individuals who are in each of the health system
    #   utilization states: out of health system (OHS), in health system (IHS),
    #   detected and treated (DT), detected and untreated (DUT)
    #   Plots the arrays as a function of age
    # Args:
    #   trace: health system utilization trace
    #   plot: if True, plots the figure
    # Returns:
    #   OHS_arr: proportion of individuals who are in the out of health system state
    #   IHS_arr: proportion of individuals who are in the in health system state
    #   DT_arr: proportion of individuals who are in the detected state
    #   DTUT_arr: proportion of individuals who are in the detected and untreated state
    #   If plot = True, plots OHS_arr, IHS_arr, DT_arr, and DUT_arr as a function of age

    N = len(trace)
    OHS_arr = []
    IHS_arr = []
    DT_arr = []
    DUT_arr = []
    for i in range(cycles + 1):
        trace_alive = trace[trace["Year" + str(i)] != "D"]
        alive_N = len(trace_alive)
        if alive_N > 0:
            OHS_arr.append(
                len(np.where(trace_alive["HSYear" + str(i)] == "OHS")[0]) / alive_N
            )
            IHS_arr.append(
                len(np.where(trace_alive["HSYear" + str(i)] == "IHS")[0]) / alive_N
            )
            DT_arr.append(
                len(np.where(trace_alive["HSYear" + str(i)] == "DT")[0]) / alive_N
            )
            DUT_arr.append(
                len(np.where(trace_alive["HSYear" + str(i)] == "DUT")[0]) / alive_N
            )
        else:
            OHS_arr.append(0)
            IHS_arr.append(0)
            DT_arr.append(0)
            DUT_arr.append(0)

    if plot == True:
        plt.figure(figsize=(8, 5))
        plt.plot(
            range(starting_age + 0, starting_age + cycles + 1),
            OHS_arr,
            color="red",
            label="Out of Health System",
        )
        plt.plot(
            range(starting_age + 0, starting_age + cycles + 1),
            IHS_arr,
            color="b",
            label="In Health System",
        )
        plt.plot(
            range(starting_age + 0, starting_age + cycles + 1),
            DT_arr,
            color="green",
            label="Detected/treated",
        )
        plt.plot(
            range(starting_age + 0, starting_age + cycles + 1),
            DUT_arr,
            color="orange",
            label="Detected/untreated",
        )
        plt.legend()
        plt.ylabel("State proportion")
        plt.xlabel("Age")
    return OHS_arr, IHS_arr, DT_arr, DUT_arr


def create_treatment_effect(trace):
    # Function:
    #   Creates dataframe with main outcomes by race and treatment (either the standard of care
    #   or the new treatment)
    #   Computes the treatment effect, the difference in main outcomes between the standard of
    #   care and the new treatment
    # Args:
    #   trace: total trace (output from run_cohort_standard or run_cohort_social_framework)
    #   which has both disease natural history and health system utilization traces
    # Returns:
    #   treatment_effect_df: a pandas dataframe on the treatment effect of the new treatment
    #   across main outcomes: life expectancy, QALYs, costs, years sick, years sick on treatment,
    #   cumulative incidence of sickness, cumulative incidence of being detected/treated

    total_arr = []
    race_groups = ["NHB", "NHW"]
    cols_of_interest = [
        "years_to_death",
        "discounted_LY",
        "QALY",
        "discounted_QALY",
        "cost",
        "discounted_cost",
        "years_sick_treated",
        "years_sick_untreated",
        "years_sick",
        "was_sick",
        "was_treated",
    ]
    for r in race_groups:
        for c in cols_of_interest:
            arr = []
            arr.append(r)
            arr.append(c)
            if c in [
                "years_to_death",
                "discounted_LY",
                "QALY",
                "discounted_QALY",
                "cost",
                "discounted_cost",
                "was_sick",
                "was_treated",
            ]:
                sc_group = trace[
                    (trace["treatment_type"] == "Standard of Care")
                    & (trace["race"] == r)
                ]
                nt_group = trace[
                    (trace["treatment_type"] == "New Treatment") & (trace["race"] == r)
                ]
            else:
                # We only compute among those who were sick for years_sick_treated and
                # years_sick_untreated
                sc_group = trace[
                    (trace["treatment_type"] == "Standard of Care")
                    & (trace["race"] == r)
                    & (trace["was_sick"] == 1)
                ]
                nt_group = trace[
                    (trace["treatment_type"] == "New Treatment")
                    & (trace["race"] == r)
                    & (trace["was_sick"] == 1)
                ]
            # For the cumulative incidences, we multiplied by 100
            if c in ["was_sick", "was_treated"]:
                sc_group[c] = sc_group[c] #* 100
                nt_group[c] = nt_group[c] #* 100

            arr.append(sc_group[c].mean())
            arr.append(sc_group[c].std() / np.sqrt(len(sc_group)))
            arr.append(nt_group[c].mean())
            arr.append(nt_group[c].std() / np.sqrt(len(nt_group)))
            arr.append((nt_group[c] - sc_group[c]).mean())
            arr.append((nt_group[c] - sc_group[c]).std() / np.sqrt(len(sc_group)))
            total_arr.append(arr)
    treatment_effect_df = pd.DataFrame(
        total_arr,
        columns=[
            "race",
            "column",
            "SC mean",
            "SC se",
            "NT mean",
            "NT se",
            "Diff mean",
            "Diff se",
        ],
    )
    return treatment_effect_df


ROUND_DIGITS = 1

def convert_to_percent(value):
    # Function:
    #   converts number into an integer percent
    # Args: 
    #   value: number to convert
    # Returns: 
    #   interger: percent

    return int(round((value*100)))

def combine_se_errors(*ses):
    # Function:
    #   Combine multiple standard errors assuming independence.
    # Args:
    #   *ses (float): One or more standard error values.
    # Returns:
    #   float: The combined standard error computed as sqrt(sum(ses_i^2)).
    
    return np.sqrt(sum(s**2 for s in ses))

def create_95_CI(variable, digits = ROUND_DIGITS):
    # Function:
    #   Create 95% confidence intervals for a float result
    # Args:
    #   variable dictionary
    #   variable["mean"]: mean point estimate
    #   variable["se"]: standard error estimate
    # Returns:
    #   String with 95% confidence interval for a float result
    
    mean, se = variable["mean"], variable["se"]
    return f" (95% CI: {round(mean - 1.96 * se, digits)}, {round(mean + 1.96 * se, digits)})"

def create_95_CI_percents(variable):
    # Function:
    #   Create 95% confidence intervals for a percent result
    # Args:
    #   variable dictionary
    #   variable["mean"]: mean point estimate
    #   variable["se"]: standard error estimate
    # Returns:
    #   String with 95% confidence interval for a percent result
    
    mean, se = variable["mean"], variable["se"]
    return f" (95% CI: {convert_to_percent(mean - 1.96 * se)}%, {convert_to_percent(mean + 1.96 * se)}%)"

def create_95_CI_costs(variable):
    # Function:
    #   Create 95% confidence intervals for a cost result
    # Args:
    #   variable dictionary
    #   variable["mean"]: mean point estimate
    #   variable["se"]: standard error estimate
    # Returns:
    #   String with 95% confidence interval for a cost result

    mean, se = variable["mean"], variable["se"]
    return f" (95% CI: {convert_to_currency(mean - 1.96*se)}, {convert_to_currency(mean + 1.96* se)})"

def format_value_and_se(value, digits=1, threshold=0.1):
 
    # Function: 
    #   Format a mean (or other point estimate) and its standard error in a standard format.
    # Args:
    #   value (float): The point estimate.
    #   se (float): The standard error.
    #   digits (int, optional): Number of decimal places to use. Default is 1.
    #   threshold (float, optional): If provided and the rounded se is less than this,
    #   then display the standard error as "<{threshold}".
    # Returns:
    #   str: A string formatted as "value [se]". For example: "75.2 [<0.1]" or "75.2 [0.3]".
   
    v = round(value['mean'], digits)
    s = round(value['se'], digits)
    if threshold is not None and s < threshold:
        se_str = f"<{threshold}"
    else:
        se_str = f"{s}"
    return f"{v} [{se_str}]"

def format_percent(value, digits=0, threshold=1):
    
    # Function:
    #   Format a value as a percentage.
    #   If the value is below the threshold (after rounding), the function returns a string
    #   such as "<1%". Otherwise it returns an integer percentage with a "%" sign.
    # Args:
    #   value (float): The percent value (in percentage points, e.g. 12.3).
    #   digits (int, optional): Rounding digits; default is 0.
    #   threshold (float, optional): Minimum display threshold; default is 1.   
    # Returns:
    #    str: The formatted percentage as "value% [SE%]"

    # Round the value to the desired number of digits.
    rounded = convert_to_percent(value['mean'])
    s = convert_to_percent(value['se'])
    if s < threshold:
        se_str = f"<{threshold}"
    else:
        se_str = f"{s}"
    return f"{rounded}% [{se_str}%]"
    
def convert_to_currency(value, digits = -2):
    # Function:
    #   Format a value as a currency
    # Args: 
    #   value (float): the cost value 
    #   digits (int, optional): rounding digits: default is -2
    # Returns:
    #   str: The formatted currency as "$value"

    return f"${int(round(value,digits)):,}"

def format_currency(value, threshold = 100, digits=-2):
    # Function:
    #   Format a value as a currency with the standard error
    #   If the value is below the threshold (after rounding), the function returns a string
    #   such as "<1%". Otherwise it returns an integer percentage with a "%" sign.
    # Args:
    #   value (float): The cost value
    #   digits (int, optional): Rounding digits; default is -2.
    #   threshold (float, optional): Minimum display threshold; default is 100.   
    # Returns:
    #    str: The formatted cost as "$value [$SE]"

    v = round(value['mean'], digits)
    s = round(value['se'], digits)
    if threshold is not None and s < threshold:
        se_str = f"<${threshold}"
    else:
        se_str = f"${int(s):,}"
    return f"${int(v):,} [{se_str}]"


## PARAMETERS USED IN ANALYSES
# cohort stage age
starting_age = 40
# we modeled yearly cycles up until age 101
# all individuals died at 100
cycles = 101 - starting_age

# Hazard ratio for increased mortality risk among those uninsured
# used in add_insurance_mortality()
# source: https://pmc.ncbi.nlm.nih.gov/articles/PMC2775760/
HAZARD_RATIO = 1.4
# racial/ethnic group-specific prevalence of uninsured individuals
# source: https://www.kff.org/racial-equity-and-health-policy/issue-brief/health-coverage-by-race-and-ethnicity/
# Non-Hispanic Black (NHB)
NHW_non_insurance_prop = 0.066
# Non-Hispanic white (NHW)
NHB_non_insurance_prop = 0.10

# Transition probabilities (standard)
##probs for out of health system to into health system
pOI = 0.05
##probs for in health system to detected/treated
pDT = 0.20
##probs for discontinuing treatment
pDTUT = 0.02
# prob from healthy to sick
pHS = 0.05

# Transition probabilities (social framework)
##probs for out of health system to into health system with insurance
pOI_ins = pOI
rrOI_no_ins = 0.20
##probs for out of health system to into health system without insurance
pOI_no_ins = convert_to_prob(convert_to_rate(pOI_ins) * rrOI_no_ins)

##probs for in health system to detected/treated with insurance
pDT_ins = pDT
rrDT_no_ins = 0.20
##probs for in health system to detected/treated without insurance
pDT_no_ins = convert_to_prob(convert_to_rate(pDT_ins) * rrDT_no_ins)

##probs for discontinuing treatment with insurance
pDTUT_ins = pDTUT
rrDTUT_no_ins = 5.0
##probs for discontinuing treatment without insurance
pDTUT_no_ins = convert_to_prob(convert_to_rate(pDTUT_ins) * rrDTUT_no_ins)

# Sickness increases mortality rates by 4
rr_SD_not_dt = 4
# Treatment effect hazard ratio
##original treatment (halves disease-specific increased mortality )
treatment_HR_SC = 0.5
##new treatment (eliminates disease-specific mortality)
treatment_HR_NT = 0.25

# Discontinuation rates
disc_rate = 0.03
v_disc = 1 / (1 + disc_rate) ** np.arange(0, cycles + 1)

# Life year (LY) mapping
#   Healthy: 1
#   Sick: 1
#   Dead: 0
mapping = {"H": 1, "S": 1, "D": 0}

# Quality-adjusted Life Year (QALY) mapping
#   Healthy: 1
#   Sick: 0.7
#   Dead: 0
QALY_H = 1.0
QALY_S = 0.7
QALY_D = 0
QALY_mapping = {"H": QALY_H, "S": QALY_S, "D": QALY_D}

# Costs mapping
#   Healthy: 100
#   Sick: 500
#   Dead: 0
COST_H = 100
COST_S = 500
COST_D = 0
COST_mapping = {"H": COST_H, "S": COST_S, "D": COST_D}

# Costs of treatment
# Standard of Care
COST_DT_SC = 20 * 12
# New Treatment
COST_DT_NT = 500 * 12
