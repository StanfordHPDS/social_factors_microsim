import os
from functions import *
from model_functions_social_framework import *
from model_functions_standard import *

# identify overall folder directory for reading/saving files
current_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(current_directory)
overall_folder = os.path.dirname(parent_directory)

# Runs the standard model with the standard of care
# These functions are defined in model_functions_standard
# SC: standard of care
HS_state_trace_df_standard_SC, state_trace_df_standard_SC, total_trace_standard_SC = (
    run_cohort_standard(False)
)
# Runs the standard model with the new treatment
HS_state_trace_df_standard_NT, state_trace_df_standard_NT, total_trace_standard_NT = (
    run_cohort_standard(True)
)

# make sure that results/standard folders exist
if not os.path.exists(f"{overall_folder}/results/standard"):
    os.makedirs(f"{overall_folder}/results/standard")
    os.makedirs(f"{overall_folder}/results/standard/sc")
    os.makedirs(f"{overall_folder}/results/standard/nt")

# export the standard of care results (SC) as csv files into results/standard/sc
HS_state_trace_df_standard_SC.to_csv(
    f"{overall_folder}/results/standard/sc/HS_state.csv", index=False
)
state_trace_df_standard_SC.to_csv(
    f"{overall_folder}/results/standard/sc/DNH_state.csv", index=False
)
total_trace_standard_SC.to_csv(
    f"{overall_folder}/results/standard/sc/total_trace.csv", index=False
)

# export the new treatment results (NT) as csv files into results/standard/nt
HS_state_trace_df_standard_NT.to_csv(
    f"{overall_folder}/results/standard/nt/HS_state.csv", index=False
)
state_trace_df_standard_NT.to_csv(
    f"{overall_folder}/results/standard/nt/DNH_state.csv", index=False
)
total_trace_standard_NT.to_csv(
    f"{overall_folder}/results/standard/nt/total_trace.csv", index=False
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
) = run_cohort_social_framework(False)
# Runs the model with our social factors framework and the new treatment
(
    HS_state_trace_df_social_framework_NT,
    state_trace_df_social_framework_NT,
    total_trace_social_framework_NT,
) = run_cohort_social_framework(True)

# export the standard of care results (SC) as csv files into Results/Standard/SC
HS_state_trace_df_social_framework_SC.to_csv(
    f"{overall_folder}/results/framework/sc/HS_state.csv", index=False
)
state_trace_df_social_framework_SC.to_csv(
    f"{overall_folder}/results/framework/sc/DNH_state.csv", index=False
)
total_trace_social_framework_SC.to_csv(
    f"{overall_folder}/results/framework/sc/total_trace.csv", index=False
)
# export the new treatment results (NT) as csv files into Results/Standard/NT
HS_state_trace_df_social_framework_NT.to_csv(
    f"{overall_folder}/results/framework/nt/HS_state.csv", index=False
)
state_trace_df_social_framework_NT.to_csv(
    f"{overall_folder}/results/framework/nt/DNH_state.csv", index=False
)
total_trace_social_framework_NT.to_csv(
    f"{overall_folder}/results/framework/nt/total_trace.csv", index=False
)
