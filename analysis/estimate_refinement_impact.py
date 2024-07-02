import pandas as pd
import numpy as np
from pathlib import Path

data_path = Path("..", "data", "aggregated_data.tsv")
data = pd.read_csv(data_path, sep="\t")

short_pdbs = ["6N35", "1C1L", "1I3H", "1KJL", "1PWB", "1SLT", "2RDK", "2ZKN", "3G83", "3P5H",
              "5GAL", "5YRG", "6H9Y", "2J1V", "2Y6G", "154L", "3AOF", "5AWQ", "5JU9", "1QFO", "2VXJ", "3NV4", "4MBY", "6HA0", "3P5G"]

ll_pdbs = ["6MSY", "2J72", "2J73", "3ACH", "4XUR", "1KQZ", "1LMQ", "1UU6", "2BOF", "4DQJ", "5GY0", "4YFZ",
           "1GNY", "1OF4", "1UXX", "2ZEX", "3OEB", "1KQY", "5VX5", "5VX9", "6UG7", "1PMH", "4HK8"]

lb_pdbs = ["1OH4", "2VUZ", "3AP9", "2J1T", "2XJR", "3ZWE", "2Z8L"]

# Calculate the mean and standard deviation of the RMSD values
mean_rmsd_rigid = data["ilrmsd_rigid"].mean()
mean_rmsd_flex = data["ilrmsd_flex"].mean()
print(f"Mean RMSD rigid: {mean_rmsd_rigid:.2f} vs Mean RMSD flexible: {mean_rmsd_flex:.2f}")

unique_pdbs = data["pdb"].unique()
n_pdbs = len(unique_pdbs)
best_model_impr = []
best_model_impr_short = []
best_model_impr_ll = []
best_model_impr_lb = []

acc_models_impr = []
for pdb in unique_pdbs:
    pdb_data = data[data["pdb"] == pdb]
    n_models = pdb_data.shape[0]
    print(f"\nPDB {pdb} has {n_models} models")
    # best model
    best_model_rigid = min(pdb_data["ilrmsd_rigid"])
    best_model_flex = min(pdb_data["ilrmsd_flex"])
    print(f"Best model for rigid: {best_model_rigid:.2f} vs Best model for flexible: {best_model_flex:.2f}")
    best_model_impr.append(best_model_rigid - best_model_flex)
    if pdb in short_pdbs:
        best_model_impr_short.append(best_model_rigid - best_model_flex)
    if pdb in ll_pdbs:
        best_model_impr_ll.append(best_model_rigid - best_model_flex)
    if pdb in lb_pdbs:
        best_model_impr_lb.append(best_model_rigid - best_model_flex)
    # std and mean
    std_rigid = pdb_data["ilrmsd_rigid"].std()
    std_flex = pdb_data["ilrmsd_flex"].std()
    mean_rigid = pdb_data["ilrmsd_rigid"].mean()
    mean_flex = pdb_data["ilrmsd_flex"].mean()
    print(f"Mean RMSD rigid: {mean_rigid:.2f} std rigid {std_rigid:.2f} vs Mean RMSD flexible: {mean_flex:.2f} std flex {std_flex:.2f}")
    # only the acceptable models
    rigid_acc = pdb_data[pdb_data["ilrmsd_rigid"] < 3.0]
    if rigid_acc.shape[0] == 0:
        print("No acceptable rigid models")
        continue
    mean_rigid_acc = rigid_acc["ilrmsd_rigid"].mean()
    mean_flex_acc = rigid_acc["ilrmsd_flex"].mean()
    print(f"Mean RMSD rigid acceptable: {mean_rigid_acc:.2f} vs Mean RMSD flexible acceptable: {mean_flex_acc:.2f}")
    # improvement
    acc_models_impr.append(mean_rigid_acc - mean_flex_acc)

print(f"\nMean improvement of the best model: {np.mean(best_model_impr):.2f}")
print(f"Mean improvement of the best model for short pdbs: {np.mean(best_model_impr_short):.2f}")
print(f"Mean improvement of the best model for ll pdbs: {np.mean(best_model_impr_ll):.2f}")
print(f"Mean improvement of the best model for lb pdbs: {np.mean(best_model_impr_lb):.2f}")

print(f"Mean improvement of the acceptable models: {np.mean(acc_models_impr):.2f}")