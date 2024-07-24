import pandas as pd
import numpy as np
import os
from haddock.libs.libplots import read_capri_table
from pathlib import Path

def get_tx(capri_ss, n):
    ilrmsd_values = capri_ss["ilrmsd"].iloc[:n]
    # is there at least one value below 3.0?
    tx_acc, tx_med, tx_high, tx_near_acc = 0, 0, 0, 0
    if ilrmsd_values[ilrmsd_values < 3.0].count() > 0:
        tx_acc = 1
    if ilrmsd_values[ilrmsd_values < 2.0].count() > 0:
        tx_med = 1
    if ilrmsd_values[ilrmsd_values < 1.0].count() > 0:
        tx_high = 1
    # near acceptable
    if ilrmsd_values[ilrmsd_values < 4.0].count() > 0:
        tx_near_acc = 1
    return tx_acc, tx_med, tx_high, tx_near_acc

def near_acceptable_models_capri(caprieval_ss):
    red_df = caprieval_ss.where(caprieval_ss["ilrmsd"] <= 4.0).dropna()
    return red_df

def acceptable_models_capri(caprieval_ss):
    red_df = caprieval_ss.where(caprieval_ss["ilrmsd"] <= 3.0).dropna()
    return red_df
    
def medium_models_capri(caprieval_ss):
    red_df = caprieval_ss.where(caprieval_ss["ilrmsd"] <= 2.0).dropna()
    return red_df

def high_models_capri(caprieval_ss):
    red_df = caprieval_ss.where(caprieval_ss["ilrmsd"] <= 1.0).dropna()
    return red_df

def acceptable_clusters_capri(caprieval_clust):
    uni_cl = np.unique(caprieval_clust["cluster_ranking"])
    acc_cl = 0
    med_cl = 0
    high_cl = 0
    near_acc_cl = 0
    for cl in uni_cl:
        cl_df = caprieval_clust.where(caprieval_clust["cluster_ranking"] == cl).dropna()
        cl_acc_len = len(acceptable_models_capri(cl_df))
        cl_med_len = len(medium_models_capri(cl_df))
        cl_high_len = len(high_models_capri(cl_df))
        cl_near_acc_len = len(near_acceptable_models_capri(cl_df))
        if cl_acc_len > 0:
            acc_cl += 1
        if cl_med_len > 0:
            med_cl += 1
        if cl_high_len > 0:
            high_cl += 1
        if cl_near_acc_len > 0:
            near_acc_cl += 1
    return acc_cl, med_cl, high_cl, near_acc_cl

# Read in the data. The DATADIR directory contains all PDB directories. In each of them, the directories of the docking runs are contained (if one runs the docking calcultations starting from the position where the cfg files are)
DATADIR="../cfg_files/"
#DATADIR="/trinity/login/aranaudo/MARCH_24/stat_ions_bound_unbound_all_glycam_conf"

pdbs = [el for el in os.listdir(DATADIR) if len(el) == 4 and el!="NOTE"]

# docking scenarios
runs = ["run_bound_default_ti-aa", "run_bound_vdw_tip-ap", "run_bound_vdw_ti-aa", "run_unbound_ens_vdw_tip-ap_clust" , "run_unbound_vdw_tip-ap_clust" ]


capri_ss_data = []
capri_clt_data = []
for pdb in pdbs:
    for run in runs:
        print(pdb, run)
        path_to_run = Path(DATADIR, pdb, run)
        caprievals = [el for el in os.listdir(path_to_run) if "caprieval" in el]
        for capri in caprievals:
            #print(capri)
            capri_ss_file = Path(path_to_run, capri, "capri_ss.tsv")
            capri_ss = read_capri_table(capri_ss_file)
            #print(capri_ss.head())
        
            for n in [1,5,10,50,100,200]:
                tx_acc, tx_med, tx_high, tx_near_acc = get_tx(capri_ss, n)
                capri_ss_data.append([pdb, run, capri, n, tx_acc, tx_med, tx_high, tx_near_acc])
            
            # check if there is only - as cluster ranking
            
            if list(np.unique(capri_ss["cluster_ranking"])) == np.array(["-"]):
                continue
            for n in [1,2,3,4,5,10,20,30,40,50]: # top interesting clusters
                capri_df_clust = capri_ss.where((capri_ss["cluster_ranking"] <= n) & (capri_ss["model-cluster_ranking"] <= 4)).dropna()
                # print(f"n is {n} and capri_df_clust is {capri_df_clust}")
                # assert capri_df_clust.shape[0] == (n+1)*4
                tx_acc, tx_med, tx_high, tx_near_acc = acceptable_clusters_capri(capri_df_clust)
                
                capri_clt_data.append([pdb, run, capri, n, tx_acc, tx_med, tx_high, tx_near_acc])
            
df_ss = pd.DataFrame(capri_ss_data, columns=["pdb", "run", "capri", "n", "tx_acc", "tx_med", "tx_high", "tx_near_acc"])
df_ss.to_csv("../data/df_ss_all_data.tsv", sep="\t", index=False)

df_clt = pd.DataFrame(capri_clt_data, columns=["pdb", "run", "capri", "n", "tx_acc", "tx_med", "tx_high", "tx_near_acc"])
df_clt.to_csv("../data/df_clt_all_data.tsv", sep="\t", index=False)
