import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

TOT_RUNS = 55
def extract_bars(df, n_list, npdbs=TOT_RUNS):
    if npdbs != TOT_RUNS:
        print(f"npdbs: {npdbs}")
    bar_acc = []
    bar_med = []
    bar_high = []
    bar_near_acc = []
    for n in n_list:
        #print(f"n: {n}")
        sr_acc = df.loc[(df["n"] == n) & (df["tx_acc"] != 0)].shape[0]/npdbs
        #print(f"sr_acc: {sr_acc}")
        bar_acc.append(sr_acc)
        sr_med = df.loc[(df["n"] == n) & (df["tx_med"] != 0)].shape[0]/npdbs
        bar_med.append(sr_med)
        sr_high = df.loc[(df["n"] == n) & (df["tx_high"] != 0)].shape[0]/npdbs
        bar_high.append(sr_high)
        # near acceptable
        sr_near_acc = df.loc[(df["n"] == n) & (df["tx_near_acc"] != 0)].shape[0]/npdbs
        bar_near_acc.append(sr_near_acc)
    return bar_acc, bar_med, bar_high, bar_near_acc

ns = [1,5,10,50,100,200]
tns = [f"T{n}" for n in ns]

ns_clust_flex = [1,2,3,4,5,10]
tns_clust_flex = [f"T{n}" for n in ns_clust_flex]

ns_clust_rigid = [1,10,20,30,40,50]
tns_clust_rigid = [f"T{n}" for n in ns_clust_rigid]

capri_ss = pd.read_csv("../data/df_ss_all_data.tsv", sep="\t")
capri_clt = pd.read_csv("../data/df_clt_all_data.tsv", sep="\t")


# define function that prints .2f values
def print_formatted_list(label, values, precision=2):
    formatted_values = [f"{value:.{precision}f}" for value in values]
    print(f"{label:<15}:", ", ".join(formatted_values))



# unbound overall
unbound_vdw_flex = capri_ss.loc[(capri_ss["run"] == "run_unbound_vdw_tip-ap_clust") & (capri_ss["capri"] == "08_caprieval")]
unbound_vdw_rigid = capri_ss.loc[(capri_ss["run"] == "run_unbound_vdw_tip-ap_clust") & (capri_ss["capri"] == "02_caprieval")]
unbound_vdw_flex_clust = capri_clt.loc[(capri_clt["run"] == "run_unbound_vdw_tip-ap_clust") & (capri_clt["capri"] == "11_caprieval")]
unbound_vdw_rigid_clust = capri_clt.loc[(capri_clt["run"] == "run_unbound_vdw_tip-ap_clust") & (capri_clt["capri"] == "06_caprieval")]

# unbound short
short_pdbs = ["6N35", "1C1L", "1I3H", "1KJL", "1PWB", "1SLT", "2RDK", "2ZKN", "3G83", "3P5H",
              "5GAL", "5YRG", "6H9Y", "2J1V", "2Y6G", "154L", "3AOF", "5AWQ", "5JU9", "1QFO", "2VXJ", "3NV4", "4MBY", "6HA0", "3P5G"]

ll_pdbs = ["6MSY", "2J72", "2J73", "3ACH", "4XUR", "1KQZ", "1LMQ", "1UU6", "2BOF", "4DQJ", "5GY0", "4YFZ",
           "1GNY", "1OF4", "1UXX", "2ZEX", "3OEB", "1KQY", "5VX5", "5VX9", "6UG7", "1PMH", "4HK8"]

lb_pdbs = ["1OH4", "2VUZ", "3AP9", "2J1T", "2XJR", "3ZWE", "2Z8L"]

unbound_vdw_flex_short = unbound_vdw_flex.loc[unbound_vdw_flex["pdb"].isin(short_pdbs)]
unbound_vdw_rigid_short = unbound_vdw_rigid.loc[unbound_vdw_rigid["pdb"].isin(short_pdbs)]
unbound_vdw_flex_clust_short = unbound_vdw_flex_clust.loc[unbound_vdw_flex_clust["pdb"].isin(short_pdbs)]
unbound_vdw_rigid_clust_short = unbound_vdw_rigid_clust.loc[unbound_vdw_rigid_clust["pdb"].isin(short_pdbs)]

unbound_vdw_flex_ll = unbound_vdw_flex.loc[unbound_vdw_flex["pdb"].isin(ll_pdbs)]
unbound_vdw_rigid_ll = unbound_vdw_rigid.loc[unbound_vdw_rigid["pdb"].isin(ll_pdbs)]
unbound_vdw_flex_clust_ll = unbound_vdw_flex_clust.loc[unbound_vdw_flex_clust["pdb"].isin(ll_pdbs)]
unbound_vdw_rigid_clust_ll = unbound_vdw_rigid_clust.loc[unbound_vdw_rigid_clust["pdb"].isin(ll_pdbs)]

unbound_vdw_flex_lb = unbound_vdw_flex.loc[unbound_vdw_flex["pdb"].isin(lb_pdbs)]
unbound_vdw_rigid_lb = unbound_vdw_rigid.loc[unbound_vdw_rigid["pdb"].isin(lb_pdbs)]
unbound_vdw_flex_clust_lb = unbound_vdw_flex_clust.loc[unbound_vdw_flex_clust["pdb"].isin(lb_pdbs)]
unbound_vdw_rigid_clust_lb = unbound_vdw_rigid_clust.loc[unbound_vdw_rigid_clust["pdb"].isin(lb_pdbs)]

width = 0.75


fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(15, 20))

print ("\nOVERALL UNBOUND DATASET")
print ("rigid overall")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_rigid, ns)
print_formatted_list("bar_high     vdw_rigid", bar_high)
print_formatted_list("bar_med      vdw_rigid", bar_med)
print_formatted_list("bar_acc      vdw_rigid", bar_acc)
print_formatted_list("bar_near_acc vdw_rigid", bar_near_acc)

r = np.arange(len(ns))
r_clust_flex = np.arange(len(ns_clust_flex))

axs[0][0].bar(r, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable (3 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 4 \mathrm{\\AA}$)')
axs[0][0].bar(r, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable (2 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 3 \mathrm{\\AA}$)')
axs[0][0].bar(r, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium (1 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 2 \mathrm{\\AA}$)')
axs[0][0].bar(r, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High ($\mathrm{IL{-}RMSD} \leq 1 \mathrm{\\AA}$)')
axs[0][0].set_ylim((0,1.01))
# set x ticks 
tns = [f"T{n}" for n in ns]
axs[0][0].set_xticks(r)
axs[0][0].set_xticklabels(tns, fontsize=16, rotation=90)
# set axs[0] yticks font size
axs[0][0].tick_params(axis='y', labelsize=16)

#print(f"unbound_vdw_rigid_clust {unbound_vdw_rigid_clust}")
print ("rigid clust overall")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_rigid_clust, ns_clust_rigid)
print_formatted_list("bar_high     vdw_rigid_clust", bar_high)
print_formatted_list("bar_med      vdw_rigid_clust", bar_med)
print_formatted_list("bar_acc      vdw_rigid_clust", bar_acc)
print_formatted_list("bar_near_acc vdw_rigid_clust", bar_near_acc)
r = np.arange(len(ns))
r_clust_flex = np.arange(len(ns_clust_flex))
r_clust_rigid = np.arange(len(ns_clust_rigid))

axs[0][1].bar(r_clust_rigid, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[0][1].bar(r_clust_rigid, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[0][1].bar(r_clust_rigid, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[0][1].bar(r_clust_rigid, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')
axs[0][1].set_ylim((0,1.01))
# set x ticks 
axs[0][1].set_xticks(r_clust_rigid)
axs[0][1].set_xticklabels(tns_clust_rigid, rotation=90)
axs[0][1].tick_params(axis='x', labelsize=16)
# set axs[0] yticks font size
axs[0][1].set_yticks([])

print ("flex overall")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_flex, ns)
print_formatted_list("bar_high     vdw_flex", bar_high)
print_formatted_list("bar_med      vdw_flex", bar_med)
print_formatted_list("bar_acc      vdw_flex", bar_acc)
print_formatted_list("bar_near_acc vdw_flex", bar_near_acc)

axs[0][2].bar(r, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[0][2].bar(r, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[0][2].bar(r, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[0][2].bar(r, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')
axs[0][2].set_ylim((0,1.01))
# set x ticks
axs[0][2].set_xticks(r)
axs[0][2].set_xticklabels(tns, fontsize=16, rotation = 90)

axs[0][2].set_yticks([])

print ("flex clust overall")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_flex_clust, ns_clust_flex)
print_formatted_list("bar_high     vdw_flex_clust", bar_high)
print_formatted_list("bar_med      vdw_flex_clust", bar_med)
print_formatted_list("bar_acc      vdw_flex_clust", bar_acc)
print_formatted_list("bar_near_acc vdw_flex_clust", bar_near_acc)

axs[0][3].bar(r_clust_flex, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[0][3].bar(r_clust_flex, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[0][3].bar(r_clust_flex, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[0][3].bar(r_clust_flex, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')
axs[0][3].set_ylim((0,1.01))
# set x ticks
axs[0][3].set_xticks(r_clust_flex)
axs[0][3].set_xticklabels(tns_clust_flex, rotation=90)
axs[0][3].tick_params(axis='x', labelsize=16)

axs[0][3].set_yticks([])

axs[0][0].set_title("rigid", fontsize=20)
axs[0][1].set_title("rigid + clustering", fontsize=20)
axs[0][2].set_title("flexref", fontsize=20)
axs[0][3].set_title("flexref + clustering", fontsize=20)


# I AM HERE----

print ("\nSHORT GLYCANS")
print ("rigid short")
# do the same for the short glycans
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_rigid_short, ns, len(short_pdbs))
print_formatted_list("bar_high     vdw_rigid_short", bar_high)
print_formatted_list("bar_med      vdw_rigid_short", bar_med)
print_formatted_list("bar_acc      vdw_rigid_short", bar_acc)
print_formatted_list("bar_near_acc vdw_rigid_short", bar_near_acc)

axs[1][0].bar(r, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[1][0].bar(r, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[1][0].bar(r, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[1][0].bar(r, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')
axs[1][0].set_ylim((0,1.01))
# set x ticks
axs[1][0].set_xticks(r)
axs[1][0].set_xticklabels(tns, fontsize=16, rotation = 90)
axs[1][0].tick_params(axis='y', labelsize=16)

print ("rigid clust short")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_rigid_clust_short, ns_clust_rigid, len(short_pdbs))
print_formatted_list("bar_high     vdw_rigid_clust_short", bar_high)
print_formatted_list("bar_med      vdw_rigid_clust_short", bar_med)
print_formatted_list("bar_acc      vdw_rigid_clust_short", bar_acc)
print_formatted_list("bar_near_acc vdw_rigid_clust_short", bar_near_acc)

axs[1][1].bar(r_clust_rigid, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[1][1].bar(r_clust_rigid, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[1][1].bar(r_clust_rigid, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[1][1].bar(r_clust_rigid, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')
axs[1][1].set_ylim((0,1.01))
# set x ticks
axs[1][1].set_xticks(r_clust_rigid)
axs[1][1].set_xticklabels(tns_clust_rigid, rotation=90)
axs[1][1].tick_params(axis='x', labelsize=16)
axs[1][1].set_yticks([])

print ("flex short")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_flex_short, ns, len(short_pdbs))
print_formatted_list("bar_high     vdw_flex_short", bar_high)
print_formatted_list("bar_med      vdw_flex_short", bar_med)
print_formatted_list("bar_acc      vdw_flex_short", bar_acc)
print_formatted_list("bar_near_acc vdw_flex_short", bar_near_acc)

axs[1][2].bar(r, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[1][2].bar(r, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[1][2].bar(r, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[1][2].bar(r, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')
axs[1][2].set_ylim((0,1.01))
# set x ticks
axs[1][2].set_xticks(r)
axs[1][2].set_xticklabels(tns, fontsize=16, rotation = 90)
axs[1][2].set_yticks([])

print ("flex clust short")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_flex_clust_short, ns_clust_flex, len(short_pdbs))
print_formatted_list("bar_high     vdw_flex_clust_short", bar_high)
print_formatted_list("bar_med      vdw_flex_clust_short", bar_med)
print_formatted_list("bar_acc      vdw_flex_clust_short", bar_acc)
print_formatted_list("bar_near_acc vdw_flex_clust_short", bar_near_acc)


axs[1][3].bar(r_clust_flex, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[1][3].bar(r_clust_flex, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[1][3].bar(r_clust_flex, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[1][3].bar(r_clust_flex, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')
axs[1][3].set_ylim((0,1.01))
# set x ticks
axs[1][3].set_xticks(r_clust_flex)
axs[1][3].set_xticklabels(tns_clust_flex, rotation=90)
axs[1][3].tick_params(axis='x', labelsize=16)
axs[1][3].set_yticks([])

# row number 2: long linear glycans
print ("\nLL GLYCANS")
print ("rigid ll")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_rigid_ll, ns, len(ll_pdbs))
print_formatted_list("bar_high     vdw_rigid_ll", bar_high)
print_formatted_list("bar_med      vdw_rigid_ll", bar_med)
print_formatted_list("bar_acc      vdw_rigid_ll", bar_acc)
print_formatted_list("bar_near_acc vdw_rigid_ll", bar_near_acc)

axs[2][0].bar(r, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[2][0].bar(r, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[2][0].bar(r, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[2][0].bar(r, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')


axs[2][0].set_ylim((0,1.01))
# set x ticks
axs[2][0].set_xticks(r)
axs[2][0].set_xticklabels(tns, fontsize=16, rotation = 90)
axs[2][0].tick_params(axis='y', labelsize=16)

print ("rigid clust ll")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_rigid_clust_ll, ns_clust_rigid, len(ll_pdbs))
print_formatted_list("bar_high     vdw_rigid_clust_ll", bar_high)
print_formatted_list("bar_med      vdw_rigid_clust_ll", bar_med)
print_formatted_list("bar_acc      vdw_rigid_clust_ll", bar_acc)
print_formatted_list("bar_near_acc vdw_rigid_clust_ll", bar_near_acc)

axs[2][1].bar(r_clust_rigid, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[2][1].bar(r_clust_rigid, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[2][1].bar(r_clust_rigid, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[2][1].bar(r_clust_rigid, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')

axs[2][1].set_ylim((0,1.01))
# set x ticks
axs[2][1].set_xticks(r_clust_rigid)
axs[2][1].set_xticklabels(tns_clust_rigid, rotation=90)
axs[2][1].tick_params(axis='x', labelsize=16)
axs[2][1].set_yticks([])

print ("flex ll")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_flex_ll, ns, len(ll_pdbs))
print_formatted_list("bar_high     vdw_flex_ll", bar_high)
print_formatted_list("bar_med      vdw_flex_ll", bar_med)
print_formatted_list("bar_acc      vdw_flex_ll", bar_acc)
print_formatted_list("bar_near_acc vdw_flex_ll", bar_near_acc)


axs[2][2].bar(r, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[2][2].bar(r, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[2][2].bar(r, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[2][2].bar(r, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')

axs[2][2].set_ylim((0,1.01))
# set x ticks
axs[2][2].set_xticks(r)
axs[2][2].set_xticklabels(tns, fontsize=16, rotation = 90)
axs[2][2].set_yticks([])

print ("flex clust ll")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_flex_clust_ll, ns_clust_flex, len(ll_pdbs))
print_formatted_list("bar_high     vdw_flex_clust_ll", bar_high)
print_formatted_list("bar_med      vdw_flex_clust_ll", bar_med)
print_formatted_list("bar_acc      vdw_flex_clust_ll", bar_acc)
print_formatted_list("bar_near_acc vdw_flex_clust_ll", bar_near_acc)

axs[2][3].bar(r_clust_flex, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[2][3].bar(r_clust_flex, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[2][3].bar(r_clust_flex, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[2][3].bar(r_clust_flex, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')

axs[2][3].set_ylim((0,1.01))
# set x ticks
axs[2][3].set_xticks(r_clust_flex)
axs[2][3].set_xticklabels(tns_clust_flex, rotation=90)
axs[2][3].tick_params(axis='x', labelsize=16)
axs[2][3].set_yticks([])



# row number 3: long branched glycans
print ("\nLB GLYCANS")
print ("rigid lb")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_rigid_lb, ns, len(lb_pdbs))
print_formatted_list("bar_high     vdw_rigid_lb", bar_high)
print_formatted_list("bar_med      vdw_rigid_lb", bar_med)
print_formatted_list("bar_acc      vdw_rigid_lb", bar_acc)
print_formatted_list("bar_near_acc vdw_rigid_lb", bar_near_acc)

axs[3][0].bar(r, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[3][0].bar(r, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[3][0].bar(r, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[3][0].bar(r, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')

axs[3][0].set_ylim((0,1.01))
# set x ticks
axs[3][0].set_xticks(r)
axs[3][0].set_xticklabels(tns, fontsize=16, rotation = 90)
axs[3][0].tick_params(axis='y', labelsize=16)

print ("rigid clust lb")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_rigid_clust_lb, ns_clust_rigid, len(lb_pdbs))
print_formatted_list("bar_high     vdw_rigid_clust_lb", bar_high)
print_formatted_list("bar_med      vdw_rigid_clust_lb", bar_med)
print_formatted_list("bar_acc      vdw_rigid_clust_lb", bar_acc)
print_formatted_list("bar_near_acc vdw_rigid_clust_lb", bar_near_acc)

axs[3][1].bar(r_clust_rigid, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[3][1].bar(r_clust_rigid, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[3][1].bar(r_clust_rigid, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[3][1].bar(r_clust_rigid, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')

axs[3][1].set_ylim((0,1.01))
# set x ticks
axs[3][1].set_xticks(r_clust_rigid)
axs[3][1].set_xticklabels(tns_clust_rigid, rotation=90)
axs[3][1].tick_params(axis='x', labelsize=16)
axs[3][1].set_yticks([])

print ("flex lb")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_flex_lb, ns, len(lb_pdbs))
print_formatted_list("bar_high     vdw_flex_lb", bar_high)
print_formatted_list("bar_med      vdw_flex_lb", bar_med)
print_formatted_list("bar_acc      vdw_flex_lb", bar_acc)
print_formatted_list("bar_near_acc vdw_flex_lb", bar_near_acc)

axs[3][2].bar(r, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[3][2].bar(r, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[3][2].bar(r, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[3][2].bar(r, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')

axs[3][2].set_ylim((0,1.01))
# set x ticks
axs[3][2].set_xticks(r)
axs[3][2].set_xticklabels(tns, fontsize=16, rotation = 90)
axs[3][2].set_yticks([])

print ("flex clust lb")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(unbound_vdw_flex_clust_lb, ns_clust_flex, len(lb_pdbs))
print_formatted_list("bar_high     vdw_flex_clust_lb", bar_high)
print_formatted_list("bar_med      vdw_flex_clust_lb", bar_med)
print_formatted_list("bar_acc      vdw_flex_clust_lb", bar_acc)
print_formatted_list("bar_near_acc vdw_flex_clust_lb", bar_near_acc)

axs[3][3].bar(r_clust_flex, bar_near_acc, color = 'lightgray',
        width = width, edgecolor = 'black',
            label='Near acceptable')
axs[3][3].bar(r_clust_flex, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable')
axs[3][3].bar(r_clust_flex, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium')
axs[3][3].bar(r_clust_flex, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High')

axs[3][3].set_ylim((0,1.01))
# set x ticks
axs[3][3].set_xticks(r_clust_flex)
axs[3][3].set_xticklabels(tns_clust_flex, rotation=90)
axs[3][3].tick_params(axis='x', labelsize=16)
axs[3][3].set_yticks([])

lines_labels = [axs[0][0].get_legend_handles_labels()]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, fontsize=18, ncol=2, loc="lower center", bbox_transform=fig.transFigure )

# give xlabels rotated horizontally
axs[0][0].set_ylabel('Full dataset\n(55 complexes)', fontsize=20)
axs[1][0].set_ylabel('SL-SB glycans\n(25 complexes)', fontsize=20)
axs[2][0].set_ylabel('LL glycans\n(23 complexes)', fontsize=20)
axs[3][0].set_ylabel('LB glycans\n(7 complexes)', fontsize=20)

y_values = [0.2, 0.4, 0.6, 0.8]
for y in y_values:
    for xdim in range(4):
        for ydim in range(4):
            axs[xdim][ydim].axhline(y=y, color='black', linestyle='-', alpha=0.1, zorder=0)

# full title for the figure
#fig.suptitle("Unbound docking, tip-ap AIRs", fontsize=24, y=1)
plt.subplots_adjust(top=0.95)


#plt.tight_layout()
plt.savefig("figures/SR_unbound.png", dpi=1200, bbox_inches="tight")
plt.close()

