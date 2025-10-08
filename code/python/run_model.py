import os
from functions import *
from model_functions_social_framework import *
from model_functions_standard import *

# identify overall folder directory for reading/saving files
current_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)
overall_folder = os.path.dirname(parent_directory)

# main parameters for the analysis
with open(f"{overall_folder}/data_and_inputs/parameters/params.pkl", "rb") as f:
    params = pickle.load(f)

# Runs the standard model with the standard of care
# These functions are defined in model_functions_standard
# SC: standard of care
HS_state_trace_df_standard_SC, state_trace_df_standard_SC, total_trace_standard_SC = (
    run_cohort_standard(params, False)
)
# Runs the standard model with the new treatment
HS_state_trace_df_standard_NT, state_trace_df_standard_NT, total_trace_standard_NT = (
    run_cohort_standard(params, True)
)

# make sure that results/standard folders exist
if not os.path.exists(f"{overall_folder}/results/standard"):
    os.makedirs(f"{overall_folder}/results/standard")
    os.makedirs(f"{overall_folder}/results/standard/sc")
    os.makedirs(f"{overall_folder}/results/standard/nt")

save_model_outputs_csv(
    overall_folder,
    "results/standard/sc",
    HS_state_trace_df_standard_SC,
    state_trace_df_standard_SC,
    total_trace_standard_SC,
)

save_model_outputs_csv(
    overall_folder,
    "results/standard/nt",
    HS_state_trace_df_standard_NT,
    state_trace_df_standard_NT,
    total_trace_standard_NT,
)


# make sure that results/framework folders exist
if not os.path.exists(f"{overall_folder}/results/framework"):
    os.makedirs(f"{overall_folder}/results/framework")
    os.makedirs(f"{overall_folder}/results/framework/sc")
    os.makedirs(f"{overall_folder}/results/framework/nt")

# Runs the model with our social factors framework and the standard of care
# These functions are defined in model_functions_social_framework
(
    HS_state_trace_df_social_framework_SC,
    state_trace_df_social_framework_SC,
    total_trace_social_framework_SC,
) = run_cohort_social_framework(params, False)
# Runs the model with our social factors framework and the new treatment
(
    HS_state_trace_df_social_framework_NT,
    state_trace_df_social_framework_NT,
    total_trace_social_framework_NT,
) = run_cohort_social_framework(params, True)


# export the new treatment results (NT) as csv files into Results/Standard/NT
save_model_outputs_csv(
    overall_folder,
    "results/framework/sc",
    HS_state_trace_df_social_framework_SC,
    state_trace_df_social_framework_SC,
    total_trace_social_framework_SC,
)


# export the new treatment results (NT) as csv files into Results/Standard/NT
save_model_outputs_csv(
    overall_folder,
    "results/framework/nt",
    HS_state_trace_df_social_framework_NT,
    state_trace_df_social_framework_NT,
    total_trace_social_framework_NT,
)


### SENSITIVITY ANALYSES

##scenario 1: disease case

# make sure that sensitivity results file exists
if not os.path.exists(f"{overall_folder}/results/sensitivity/"):
    os.makedirs(f"{overall_folder}/results/sensitivity/disease")
    os.makedirs(f"{overall_folder}/results/sensitivity/disease/standard/sc")
    os.makedirs(f"{overall_folder}/results/sensitivity/disease/standard/nt")
    os.makedirs(f"{overall_folder}/results/sensitivity/disease/framework/sc")
    os.makedirs(f"{overall_folder}/results/sensitivity/disease/framework/nt")

# params for the sensitivity analysis
with open(f"{overall_folder}/data_and_inputs/parameters/params_sens_1.pkl", "rb") as f:
    params = pickle.load(f)

# Runs the standard model with the standard of care under new disease parameters
# These functions are defined in model_functions_standard
# SC: standard of care
HS_state_trace_df_standard_SC, state_trace_df_standard_SC, total_trace_standard_SC = (
    run_cohort_standard(params, False)
)
# Runs the standard model with the new treatment
HS_state_trace_df_standard_NT, state_trace_df_standard_NT, total_trace_standard_NT = (
    run_cohort_standard(params, True)
)


save_model_outputs_csv(
    overall_folder,
    "results/sensitivity/disease/standard/sc",
    HS_state_trace_df_standard_SC,
    state_trace_df_standard_SC,
    total_trace_standard_SC,
)

save_model_outputs_csv(
    overall_folder,
    "results/sensitivity/disease/standard/nt",
    HS_state_trace_df_standard_NT,
    state_trace_df_standard_NT,
    total_trace_standard_NT,
)


(
    HS_state_trace_df_social_framework_SC,
    state_trace_df_social_framework_SC,
    total_trace_social_framework_SC,
) = run_cohort_social_framework(params, False)

(
    HS_state_trace_df_social_framework_NT,
    state_trace_df_social_framework_NT,
    total_trace_social_framework_NT,
) = run_cohort_social_framework(params, True)

# export the new treatment results (NT) as csv files into Results/Standard/NT
save_model_outputs_csv(
    overall_folder,
    "results/sensitivity/disease/framework/sc",
    HS_state_trace_df_social_framework_SC,
    state_trace_df_social_framework_SC,
    total_trace_social_framework_SC,
)


# export the new treatment results (NT) as csv files into Results/Standard/NT
save_model_outputs_csv(
    overall_folder,
    "results/sensitivity/disease/framework/nt",
    HS_state_trace_df_social_framework_NT,
    state_trace_df_social_framework_NT,
    total_trace_social_framework_NT,
)


## SCENARIO 2: differential costs for those without insurance
# make sure that sensitivity costs folder exists
if not os.path.exists(f"{overall_folder}/results/sensitivity/costs"):
    os.makedirs(f"{overall_folder}/results/sensitivity/costs")
    os.makedirs(f"{overall_folder}/results/sensitivity/costs/standard/sc")
    os.makedirs(f"{overall_folder}/results/sensitivity/costs/standard/nt")
    os.makedirs(f"{overall_folder}/results/sensitivity/costs/framework/sc")
    os.makedirs(f"{overall_folder}/results/sensitivity/costs/framework/nt")

# params for the sensitivity analysis
with open(f"{overall_folder}/data_and_inputs/parameters/params_sens_2.pkl", "rb") as f:
    params = pickle.load(f)

# These functions are defined in model_functions_standard
# SC: standard of care
HS_state_trace_df_standard_SC, state_trace_df_standard_SC, total_trace_standard_SC = (
    run_cohort_standard(params, False)
)
# Runs the standard model with the new treatment
HS_state_trace_df_standard_NT, state_trace_df_standard_NT, total_trace_standard_NT = (
    run_cohort_standard(params, True)
)


save_model_outputs_csv(
    overall_folder,
    "results/sensitivity/costs/standard/sc",
    HS_state_trace_df_standard_SC,
    state_trace_df_standard_SC,
    total_trace_standard_SC,
)

save_model_outputs_csv(
    overall_folder,
    "results/sensitivity/costs/standard/nt",
    HS_state_trace_df_standard_NT,
    state_trace_df_standard_NT,
    total_trace_standard_NT,
)


(
    HS_state_trace_df_social_framework_SC,
    state_trace_df_social_framework_SC,
    total_trace_social_framework_SC,
) = run_cohort_social_framework(params, False)

(
    HS_state_trace_df_social_framework_NT,
    state_trace_df_social_framework_NT,
    total_trace_social_framework_NT,
) = run_cohort_social_framework(params, True)

# export the new treatment results (NT) as csv files into Results/Standard/NT
save_model_outputs_csv(
    overall_folder,
    "results/sensitivity/costs/framework/sc",
    HS_state_trace_df_social_framework_SC,
    state_trace_df_social_framework_SC,
    total_trace_social_framework_SC,
)


# export the new treatment results (NT) as csv files into Results/Standard/NT
save_model_outputs_csv(
    overall_folder,
    "results/sensitivity/costs/framework/nt",
    HS_state_trace_df_social_framework_NT,
    state_trace_df_social_framework_NT,
    total_trace_social_framework_NT,
)
