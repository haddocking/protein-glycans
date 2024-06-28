import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

TOT_RUNS = 89
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

ns_clust_flex = [1,2,3,4,5]
tns_clust_flex = [f"T{n}" for n in ns_clust_flex]

ns_clust_rigid = [1,10,20,30,40,50]
tns_clust_rigid = [f"T{n}" for n in ns_clust_rigid]

capri_ss = pd.read_csv("../data/df_ss_all_data.tsv", sep="\t")
capri_clt = pd.read_csv("../data/df_clt_all_data.tsv", sep="\t")

# define function that prints .2f values
def print_formatted_list(label, values, precision=2):
    formatted_values = [f"{value:.{precision}f}" for value in values]
    print(f"{label:<15}:", ", ".join(formatted_values))


# bound, 1st line ti-aa, 2nd line tip-ap. columns left to right sl, sb, ll, lb
bound_vdw_ti = capri_ss.loc[(capri_ss["run"] == "run_bound_vdw_ti") & (capri_ss["capri"] == "2_caprieval")]
bound_vdw_na = capri_ss.loc[(capri_ss["run"] == "run_bound_vdw_na") & (capri_ss["capri"] == "2_caprieval")]

# categories
sl_pdbs= ["3OAU", "1WU6", "3N17", "1W6P", "2IT6", "3VV1", "4R9F", "5T4Z", "2XOM", "4QPW", "4D5I", "2G7C", "2YP3", "5HZB", "6N35", "1C1L", "1I3H", "1KJL", "1PWB", "1SLT", "2RDK", "2ZKN", "3G83", "3P5H", "5GAL", "5YRG", "6H9Y", "2J1V", "2Y6G", "154L","3AOF", "5AWQ", "5JU9", "1QFO", "2VXJ", "3NV4", "4MBY", "6HA0" ]

sb_pdbs= [ "1UZ8", "1JPC", "2WRA", "5HZA", "5V6F", "3P5G" ]

ll_pdbs= [ "6R3M", "1JDC", "3WH1", "4YG0", "6BE4", "1W8U", "2WAB", "2YP4", "1GUI", "1GWL", "1GWM", "6MSY", "2J72", "2J73", "3ACH", "4XUR", "1KQZ", "1LMQ", "1UU6", "2BOF", "4DQJ", "5GY0", "4YFZ", "1GNY", "1OF4", "1UXX", "2ZEX", "3OEB", "1KQY", "5VX5", "5VX9", "6UG7", "1PMH", "4HK8"]

lb_pdbs= [ "1S3K", "1SL5", "2I74", "2CHB", "2J1T", "2XJR", "3ZWE", "2Z8L", "3AP9", "1OH4","2VUZ"]

# locate
bound_vdw_ti_sl = bound_vdw_ti.loc[bound_vdw_ti["pdb"].isin(sl_pdbs)]
bound_vdw_ti_sb = bound_vdw_ti.loc[bound_vdw_ti["pdb"].isin(sb_pdbs)]
bound_vdw_ti_ll = bound_vdw_ti.loc[bound_vdw_ti["pdb"].isin(ll_pdbs)]
bound_vdw_ti_lb = bound_vdw_ti.loc[bound_vdw_ti["pdb"].isin(lb_pdbs)]


bound_vdw_na_sl = bound_vdw_na.loc[bound_vdw_na["pdb"].isin(sl_pdbs)]
bound_vdw_na_sb = bound_vdw_na.loc[bound_vdw_na["pdb"].isin(sb_pdbs)]
bound_vdw_na_ll = bound_vdw_na.loc[bound_vdw_na["pdb"].isin(ll_pdbs)]
bound_vdw_na_lb = bound_vdw_na.loc[bound_vdw_na["pdb"].isin(lb_pdbs)]

width = 0.75
fig, axs = plt.subplots(nrows=4, ncols=2, figsize=(9, 20))

#1st row
print("ti-aa")
print("\nti-aa SL")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(bound_vdw_ti_sl, ns, len(sl_pdbs))
print_formatted_list("bar_high     vdw_ti-aa", bar_high)
print_formatted_list("bar_med      vdw_ti-aa", bar_med)
print_formatted_list("bar_acc      vdw_ti-aa", bar_acc)
print_formatted_list("bar_near_acc vdw_ti-aa", bar_near_acc)

r = np.arange(len(ns))
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
axs[0][0].set_xticklabels(tns, fontsize=16, rotation = 90)
# set axs[0] yticks font size
axs[0][0].tick_params(axis='y', labelsize=16)


print("\nti-aa SB")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(bound_vdw_ti_sb, ns,  len(sb_pdbs))
print_formatted_list("bar_high     vdw_ti-aa", bar_high)
print_formatted_list("bar_med      vdw_ti-aa", bar_med)
print_formatted_list("bar_acc      vdw_ti-aa", bar_acc)
print_formatted_list("bar_near_acc vdw_ti-aa", bar_near_acc)

r = np.arange(len(ns))
axs[1][0].bar(r, bar_near_acc, color = 'lightgray',
          width = width, edgecolor = 'black',
          label='Near acceptable (3 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 4 \mathrm{\\AA}$)')
axs[1][0].bar(r, bar_acc, color = '#a5cee2',                                                   
    	  width = width, edgecolor = 'black',
          label='Acceptable (2 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 3 \mathrm{\\AA}$)')
axs[1][0].bar(r, bar_med, color = '#b2df8a',
          width = width, edgecolor = 'black',
          label='Medium (1 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 2 \mathrm{\\AA}$)')
axs[1][0].bar(r, bar_high, color = '#33a02b',
          width = width, edgecolor = 'black',
          label='High ($\mathrm{IL{-}RMSD} \leq 1 \mathrm{\\AA}$)')
axs[1][0].set_ylim((0,1.01))
# set x ticks
tns = [f"T{n}" for n in ns]
axs[1][0].set_xticks(r)
axs[1][0].set_xticklabels(tns, fontsize=16, rotation = 90)
# set axs[0] yticks font size
axs[1][0].tick_params(axis='y', labelsize=16)

print("\nti-aa LL")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(bound_vdw_ti_ll, ns,  len(ll_pdbs))
print_formatted_list("bar_high     vdw_ti-aa", bar_high)
print_formatted_list("bar_med      vdw_ti-aa", bar_med)
print_formatted_list("bar_acc      vdw_ti-aa", bar_acc)
print_formatted_list("bar_near_acc vdw_ti-aa", bar_near_acc)

r = np.arange(len(ns))
axs[2][0].bar(r, bar_near_acc, color = 'lightgray',
          width = width, edgecolor = 'black',
          label='Near acceptable (3 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 4 \mathrm{\\AA}$)')
axs[2][0].bar(r, bar_acc, color = '#a5cee2',
          width = width, edgecolor = 'black',
          label='Acceptable (2 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 3 \mathrm{\\AA}$)')
axs[2][0].bar(r, bar_med, color = '#b2df8a',
          width = width, edgecolor = 'black',
          label='Medium (1 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 2 \mathrm{\\AA}$)')
axs[2][0].bar(r, bar_high, color = '#33a02b',
          width = width, edgecolor = 'black',
          label='High ($\mathrm{IL{-}RMSD} \leq 1 \mathrm{\\AA}$)')
axs[2][0].set_ylim((0,1.01))
# set x ticks
tns = [f"T{n}" for n in ns]
axs[2][0].set_xticks(r)
axs[2][0].set_xticklabels(tns, fontsize=16, rotation = 90)
# set axs[0] yticks font size
axs[2][0].tick_params(axis='y', labelsize=16)



print("\nti-aa LB")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(bound_vdw_ti_lb, ns,  len(lb_pdbs))
print_formatted_list("bar_high     vdw_ti-aa", bar_high)
print_formatted_list("bar_med      vdw_ti-aa", bar_med)
print_formatted_list("bar_acc      vdw_ti-aa", bar_acc)
print_formatted_list("bar_near_acc vdw_ti-aa", bar_near_acc)

r = np.arange(len(ns))
axs[3][0].bar(r, bar_near_acc, color = 'lightgray',
          width = width, edgecolor = 'black',
          label='Near acceptable (3 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 4 \mathrm{\\AA}$)')
axs[3][0].bar(r, bar_acc, color = '#a5cee2',
          width = width, edgecolor = 'black',
          label='Acceptable (2 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 3 \mathrm{\\AA}$)')
axs[3][0].bar(r, bar_med, color = '#b2df8a',
          width = width, edgecolor = 'black',
          label='Medium (1 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 2 \mathrm{\\AA}$)')
axs[3][0].bar(r, bar_high, color = '#33a02b',
          width = width, edgecolor = 'black',
          label='High ($\mathrm{IL{-}RMSD} \leq 1 \mathrm{\\AA}$)')
axs[3][0].set_ylim((0,1.01))
# set x ticks
tns = [f"T{n}" for n in ns]
axs[3][0].set_xticks(r)
axs[3][0].set_xticklabels(tns, fontsize=16, rotation = 90)
# set axs[0] yticks font size
axs[3][0].tick_params(axis='y', labelsize=16)



# 2nd row, tip-ap , per cat
print("tip-ap")
print("\ntip-ap SL")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(bound_vdw_na_sl, ns,  len(sl_pdbs))
print_formatted_list("bar_high     vdw_tip-ap", bar_high)
print_formatted_list("bar_med      vdw_tip-ap", bar_med)
print_formatted_list("bar_acc      vdw_tip-ap", bar_acc)
print_formatted_list("bar_near_acc vdw_tip-ap", bar_near_acc)

r = np.arange(len(ns))
axs[0][1].bar(r, bar_near_acc, color = 'lightgray',
          width = width, edgecolor = 'black',
          label='Near acceptable (3 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 4 \mathrm{\\AA}$)')
axs[0][1].bar(r, bar_acc, color = '#a5cee2',                                                   
    	  width = width, edgecolor = 'black',
          label='Acceptable (2 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 3 \mathrm{\\AA}$)')
axs[0][1].bar(r, bar_med, color = '#b2df8a',
          width = width, edgecolor = 'black',
          label='Medium (1 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 2 \mathrm{\\AA}$)')
axs[0][1].bar(r, bar_high, color = '#33a02b',
          width = width, edgecolor = 'black',
          label='High ($\mathrm{IL{-}RMSD} \leq 1 \mathrm{\\AA}$)')
axs[0][1].set_ylim((0,1.01))
# set x ticks
tns = [f"T{n}" for n in ns]
axs[0][1].set_xticks(r)
axs[0][1].set_xticklabels(tns, fontsize=16, rotation = 90)
# set axs[0] yticks font size
axs[0][1].tick_params(axis='y', labelsize=16)


print("\ntip-ap SB")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(bound_vdw_na_sb, ns,  len(sb_pdbs))
print_formatted_list("bar_high     vdw_tip-ap", bar_high)
print_formatted_list("bar_med      vdw_tip-ap", bar_med)
print_formatted_list("bar_acc      vdw_tip-ap", bar_acc)
print_formatted_list("bar_near_acc vdw_tip-ap", bar_near_acc)

r = np.arange(len(ns))
axs[1][1].bar(r, bar_near_acc, color = 'lightgray',
          width = width, edgecolor = 'black',
          label='Near acceptable (3 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 4 \mathrm{\\AA}$)')
axs[1][1].bar(r, bar_acc, color = '#a5cee2',                                                   
    	  width = width, edgecolor = 'black',
          label='Acceptable (2 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 3 \mathrm{\\AA}$)')
axs[1][1].bar(r, bar_med, color = '#b2df8a',
          width = width, edgecolor = 'black',
          label='Medium (1 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 2 \mathrm{\\AA}$)')
axs[1][1].bar(r, bar_high, color = '#33a02b',
          width = width, edgecolor = 'black',
          label='High ($\mathrm{IL{-}RMSD} \leq 1 \mathrm{\\AA}$)')
axs[1][1].set_ylim((0,1.01))
# set x ticks
tns = [f"T{n}" for n in ns]
axs[1][1].set_xticks(r)
axs[1][1].set_xticklabels(tns, fontsize=16, rotation = 90)
# set axs[0] yticks font size
axs[1][1].tick_params(axis='y', labelsize=16)

print("\ntip-ap LL")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(bound_vdw_na_ll, ns,  len(ll_pdbs))
print_formatted_list("bar_high     vdw_tip-ap", bar_high)
print_formatted_list("bar_med      vdw_tip-ap", bar_med)
print_formatted_list("bar_acc      vdw_tip-ap", bar_acc)
print_formatted_list("bar_near_acc vdw_tip-ap", bar_near_acc)

r = np.arange(len(ns))
axs[2][1].bar(r, bar_near_acc, color = 'lightgray',
          width = width, edgecolor = 'black',
          label='Near acceptable (3 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 4 \mathrm{\\AA}$)')
axs[2][1].bar(r, bar_acc, color = '#a5cee2',
          width = width, edgecolor = 'black',
          label='Acceptable (2 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 3 \mathrm{\\AA}$)')
axs[2][1].bar(r, bar_med, color = '#b2df8a',
          width = width, edgecolor = 'black',
          label='Medium (1 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 2 \mathrm{\\AA}$)')
axs[2][1].bar(r, bar_high, color = '#33a02b',
          width = width, edgecolor = 'black',
          label='High ($\mathrm{IL{-}RMSD} \leq 1 \mathrm{\\AA}$)')
axs[2][1].set_ylim((0,1.01))
# set x ticks
tns = [f"T{n}" for n in ns]
axs[2][1].set_xticks(r)
axs[2][1].set_xticklabels(tns, fontsize=16, rotation = 90)
# set axs[0] yticks font size
axs[2][1].tick_params(axis='y', labelsize=16)



print("\ntip-ap LB")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(bound_vdw_na_lb, ns,  len(lb_pdbs))
print_formatted_list("bar_high     vdw_tip-ap", bar_high)
print_formatted_list("bar_med      vdw_tip-ap", bar_med)
print_formatted_list("bar_acc      vdw_tip-ap", bar_acc)
print_formatted_list("bar_near_acc vdw_tip-ap", bar_near_acc)

r = np.arange(len(ns))
axs[3][1].bar(r, bar_near_acc, color = 'lightgray',
          width = width, edgecolor = 'black',
          label='Near acceptable (3 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 4 \mathrm{\\AA}$)')
axs[3][1].bar(r, bar_acc, color = '#a5cee2',
          width = width, edgecolor = 'black',
          label='Acceptable (2 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 3 \mathrm{\\AA}$)')
axs[3][1].bar(r, bar_med, color = '#b2df8a',
          width = width, edgecolor = 'black',
          label='Medium (1 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 2 \mathrm{\\AA}$)')
axs[3][1].bar(r, bar_high, color = '#33a02b',
          width = width, edgecolor = 'black',
          label='High ($\mathrm{IL{-}RMSD} \leq 1 \mathrm{\\AA}$)')
axs[3][1].set_ylim((0,1.01))
# set x ticks
tns = [f"T{n}" for n in ns]
axs[3][1].set_xticks(r)
axs[3][1].set_xticklabels(tns, fontsize=16, rotation = 90)
# set axs[0] yticks font size
axs[3][1].tick_params(axis='y', labelsize=16)


# give x labels rotated horizontally
axs[0][0].set_ylabel("SL glycans\n(38 complexes)", fontsize = 20)
axs[1][0].set_ylabel("SB glycans\n(6 complexes)", fontsize = 20)
axs[2][0].set_ylabel("LL glycans\n(34 complexes)", fontsize = 20)
axs[3][0].set_ylabel("LB glycans\n(11 complexes)", fontsize = 20)


axs[0][0].set_title("ti-aa AIRs", fontsize = 20)
axs[0][1].set_title("tip-ap AIRs", fontsize = 20)



# prob exp
lines_labels = [axs[0][0].get_legend_handles_labels()]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, fontsize=18, ncol=2, loc="lower center", bbox_transform=fig.transFigure )

# full title
#fig.suptitle("Bound docking, vdW scoring function", fontsize = 24, y = 1)
plt.subplots_adjust(top=0.95)

y_values = [0.2, 0.4, 0.6, 0.8]
for y in y_values:
    for xdim in range(4):
        for ydim in range(2):
            axs[xdim][ydim].axhline(y=y, color='black', linestyle='-', alpha=0.1, zorder=0)


#plt.tight_layout()
plt.savefig("figures/SR_bound_per_cat_vdw_ti-aa_vs_tip-ap.png", dpi=1200, bbox_inches="tight")
plt.close()


