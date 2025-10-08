import os
import pickle
from functions import *


# identify overall folder directory for reading/saving files
current_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)
overall_folder = os.path.dirname(parent_directory)

## parameters for main analysis
params = {
    "starting_age": 40,
    "cycles": 101 - 40,  # all individuals died at 100
    # Hazard ratio for increased mortality risk among those uninsured
    # used in add_insurance_mortality()
    # source: https://pmc.ncbi.nlm.nih.gov/articles/PMC2775760/
    "HAZARD_RATIO": 1.4,
    # racial/ethnic group-specific prevalence of uninsured individuals
    # source: https://www.kff.org/racial-equity-and-health-policy/issue-brief/health-coverage-by-race-and-ethnicity/
    "NHW_non_insurance_prop": 0.066,
    "NHB_non_insurance_prop": 0.10,
    "pOI": 0.05,  ##probs for out of health system to into health system
    "pDT": 0.20,  ##probs for in health system to detected/treated
    "pDTUT": 0.02,  ##probs for discontinuing treatment
    "pHS": 0.05,  # prob from healthy to sick
    "pOI_ins": 0.05,  ##probs for out of health system to into health system with insurance
    "pDT_ins": 0.20,  ##probs for in health system to detected/treated with insurance
    "pDTUT_ins": 0.02,  ##probs for discontinuing treatment with insurance
    "rrOI_no_ins": 0.20,
    "pOI_no_ins": None,  ##probs for out of health system to into health system without insurance
    "rrDT_no_ins": 0.20,
    "pDT_no_ins": None,  ##probs for in health system to detected/treated without insurance
    "rrDTUT_no_ins": 5.0,
    "pDTUT_no_ins": None,  ##probs for discontinuing treatment without insurance
    "rr_SD_not_dt": 4,  # Sickness increases mortality rates by 4
    "treatment_HR_SC": 0.5,  ##original treatment (halves disease-specific increased mortality )
    "treatment_HR_NT": 0.25,  ##new treatment (eliminates disease-specific mortality)
    "disc_rate": 0.03,  # Discontinuation rates
    "mapping": {"H": 1, "S": 1, "D": 0},  # Life year (LY) mapping
    "QALY_mapping": {
        "H": 1.0,
        "S": 0.7,
        "D": 0.0,
    },  # Quality-adjusted Life Year (QALY) mapping
    "COST_mapping": {"H": 100, "S": 500, "D": 0},  # Costs mapping
    "COST_DT_SC": 20 * 12,  # Standard of Care
    "COST_DT_NT": 500 * 12,  # New treatment
    "COST_S_no_ins": 0,  # uninsured individuals have extra cost
    "COST_DT_multiplier_no_ins": 1,  # treatment costs more for uninsured
}

params["pOI_no_ins"] = convert_to_prob(
    convert_to_rate(params["pOI_ins"]) * params["rrOI_no_ins"]
)

params["pDT_no_ins"] = convert_to_prob(
    convert_to_rate(params["pDT_ins"]) * params["rrDT_no_ins"]
)

params["pDTUT_no_ins"] = convert_to_prob(
    convert_to_rate(params["pDTUT_ins"]) * params["rrDTUT_no_ins"]
)


# export cohort dataframe into results folder
if not os.path.exists(f"{overall_folder}/data_and_inputs/parameters/"):
    os.makedirs(f"{overall_folder}/data_and_inputs/parameters/")
with open(f"{overall_folder}/data_and_inputs/parameters/params.pkl", "wb") as f:
    pickle.dump(params, f)

##Sensitivity analysis

# scenario 1: "another case of disease"
# low prevalence, high burden of mortality
params["pHS"] = 0.001
params["rr_SD_not_dt"] = 6
params["QALY_mapping"] = {"H": 1.0, "S": 0.5, "D": 0.0}
params["COST_mapping"] = {"H": 100, "S": 5000, "D": 0}

with open(f"{overall_folder}/data_and_inputs/parameters/params_sens_1.pkl", "wb") as f:
    pickle.dump(params, f)


##scenario 2: additional costs for those without insurance
params["pHS"] = 0.05
params["rr_SD_not_dt"] = 4
params["QALY_mapping"] = {"H": 1.0, "S": 0.7, "D": 0.0}
params["COST_mapping"] = {"H": 100, "S": 500, "D": 0}
params["COST_S_no_ins"] = 1500
params["COST_DT_multiplier_no_ins"] = 4

with open(f"{overall_folder}/data_and_inputs/parameters/params_sens_2.pkl", "wb") as f:
    pickle.dump(params, f)
