import pandas as pd
import numpy as np
from pathlib import Path

def load_data(filepath):
    return pd.read_csv(filepath, sep="\t")

def calculate_mean_rmsd(data):
    mean_rmsd_rigid = data["ilrmsd_rigid"].mean()
    mean_rmsd_flex = data["ilrmsd_flex"].mean()
    print(f"Mean RMSD rigid: {mean_rmsd_rigid:.2f} vs Mean RMSD flexible: {mean_rmsd_flex:.2f}")
    return mean_rmsd_rigid, mean_rmsd_flex

def process_pdb_data(data, pdb, short_pdbs, ll_pdbs, lb_pdbs):
    pdb_data = data[data["pdb"] == pdb]
    n_models = pdb_data.shape[0]
    print(f"\nPDB {pdb} has {n_models} models")

    best_model_rigid = min(pdb_data["ilrmsd_rigid"])
    best_model_flex = min(pdb_data["ilrmsd_flex"])
    print(f"Best model for rigid: {best_model_rigid:.2f} vs Best model for flexible: {best_model_flex:.2f}")

    improvement = best_model_rigid - best_model_flex
    best_model_impr = {'overall': improvement}

    if pdb in short_pdbs:
        best_model_impr['short'] = improvement
    if pdb in ll_pdbs:
        best_model_impr['ll'] = improvement
    if pdb in lb_pdbs:
        best_model_impr['lb'] = improvement

    std_rigid = pdb_data["ilrmsd_rigid"].std()
    std_flex = pdb_data["ilrmsd_flex"].std()
    mean_rigid = pdb_data["ilrmsd_rigid"].mean()
    mean_flex = pdb_data["ilrmsd_flex"].mean()
    print(f"Mean RMSD rigid: {mean_rigid:.2f} std rigid {std_rigid:.2f} vs Mean RMSD flexible: {mean_flex:.2f} std flex {std_flex:.2f}")

    rigid_acc = pdb_data[pdb_data["ilrmsd_rigid"] < 3.0]
    if rigid_acc.shape[0] == 0:
        print("No acceptable rigid models")
        return best_model_impr, None

    mean_rigid_acc = rigid_acc["ilrmsd_rigid"].mean()
    mean_flex_acc = rigid_acc["ilrmsd_flex"].mean()
    print(f"Mean RMSD rigid acceptable: {mean_rigid_acc:.2f} vs Mean RMSD flexible acceptable: {mean_flex_acc:.2f}")

    acc_improvement = mean_rigid_acc - mean_flex_acc
    return best_model_impr, acc_improvement

def main():
    data_path = Path("..", "data", "aggregated_data.tsv")
    data = load_data(data_path)

    short_pdbs = ["6N35", "1C1L", "1I3H", "1KJL", "1PWB", "1SLT", "2RDK", "2ZKN", "3G83", "3P5H",
                  "5GAL", "5YRG", "6H9Y", "2J1V", "2Y6G", "154L", "3AOF", "5AWQ", "5JU9", "1QFO", "2VXJ", "3NV4", "4MBY", "6HA0", "3P5G"]
    ll_pdbs = ["6MSY", "2J72", "2J73", "3ACH", "4XUR", "1KQZ", "1LMQ", "1UU6", "2BOF", "4DQJ", "5GY0", "4YFZ",
               "1GNY", "1OF4", "1UXX", "2ZEX", "3OEB", "1KQY", "5VX5", "5VX9", "6UG7", "1PMH", "4HK8"]
    lb_pdbs = ["1OH4", "2VUZ", "3AP9", "2J1T", "2XJR", "3ZWE", "2Z8L"]

    calculate_mean_rmsd(data)

    unique_pdbs = data["pdb"].unique()
    best_model_impr = {'overall': {}, 'short': {}, 'll': {}, 'lb': {}}
    acc_models_impr = []

    for pdb in unique_pdbs:
        best_impr, acc_impr = process_pdb_data(data, pdb, short_pdbs, ll_pdbs, lb_pdbs)
        best_model_impr['overall'][pdb] = best_impr['overall']
        if 'short' in best_impr:
            best_model_impr['short'][pdb] = best_impr['short']
        if 'll' in best_impr:
            best_model_impr['ll'][pdb] = best_impr['ll']
        if 'lb' in best_impr:
            best_model_impr['lb'][pdb] = best_impr['lb']
        if acc_impr is not None:
            acc_models_impr.append((pdb, acc_impr))

    print(f"\nMean improvement of the best model: {np.mean(list(best_model_impr['overall'].values())):.2f}")
    if best_model_impr['short']:
        print(f"Mean improvement of the best model for short pdbs: {np.mean(list(best_model_impr['short'].values())):.2f}")
    if best_model_impr['ll']:
        print(f"Mean improvement of the best model for ll pdbs: {np.mean(list(best_model_impr['ll'].values())):.2f}")
    if best_model_impr['lb']:
        print(f"Mean improvement of the best model for lb pdbs: {np.mean(list(best_model_impr['lb'].values())):.2f}")

    if acc_models_impr:
        print(f"Mean improvement of the acceptable models: {np.mean([impr for _, impr in acc_models_impr]):.2f}")

    # Max improvement and the corresponding PDB IDs
    max_overall_impr_pdb = max(best_model_impr['overall'], key=best_model_impr['overall'].get)
    print(f"\nMax improvement of the best model: {np.max(list(best_model_impr['overall'].values())):.2f} (PDB: {max_overall_impr_pdb})")
    if best_model_impr['short']:
        max_short_impr_pdb = max(best_model_impr['short'], key=best_model_impr['short'].get)
        print(f"Max improvement of the best model for short pdbs: {np.max(list(best_model_impr['short'].values())):.2f} (PDB: {max_short_impr_pdb})")
    if best_model_impr['ll']:
        max_ll_impr_pdb = max(best_model_impr['ll'], key=best_model_impr['ll'].get)
        print(f"Max improvement of the best model for ll pdbs: {np.max(list(best_model_impr['ll'].values())):.2f} (PDB: {max_ll_impr_pdb})")
    if best_model_impr['lb']:
        max_lb_impr_pdb = max(best_model_impr['lb'], key=best_model_impr['lb'].get)
        print(f"Max improvement of the best model for lb pdbs: {np.max(list(best_model_impr['lb'].values())):.2f} (PDB: {max_lb_impr_pdb})")

    if acc_models_impr:
        max_acc_impr_pdb = max(acc_models_impr, key=lambda x: x[1])[0]
        print(f"Max improvement of the acceptable models: {np.max([impr for _, impr in acc_models_impr]):.2f} (PDB: {max_acc_impr_pdb})")

if __name__ == "__main__":
    main()

