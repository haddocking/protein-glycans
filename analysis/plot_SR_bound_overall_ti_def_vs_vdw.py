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


# bound default vs vdw (true interface)
bound_default_ti = capri_ss.loc[(capri_ss["run"] == "run_bound_default_ti") & (capri_ss["capri"] == "2_caprieval")]
bound_vdw_ti = capri_ss.loc[(capri_ss["run"] == "run_bound_vdw_ti") & (capri_ss["capri"] == "2_caprieval")]

width = 0.75

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 9))


print("OVERALL BOUND")
print("\n default ti rigid")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(bound_default_ti, ns)
print_formatted_list("bar_high     def_ti_rigid", bar_high)
print_formatted_list("bar_med      def_ti_rigid", bar_med)
print_formatted_list("bar_acc      def_ti_rigid", bar_acc)
print_formatted_list("bar_near_acc def_ti_rigid", bar_near_acc)

r = np.arange(len(ns))
axs[0].bar(r, bar_near_acc, color = 'lightgray',
            width = width, edgecolor = 'black',
            label='Near acceptable (3 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 4 \mathrm{\\AA}$)')
axs[0].bar(r, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable (2 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 3 \mathrm{\\AA}$)')
axs[0].bar(r, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium (1 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 2 \mathrm{\\AA}$)')
axs[0].bar(r, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High ($\mathrm{IL{-}RMSD} \leq 1 \mathrm{\\AA}$)')
axs[0].set_ylim((0,1.01))
# set x ticks 
tns = [f"T{n}" for n in ns]
axs[0].set_xticks(r)
axs[0].set_xticklabels(tns, fontsize=16, rotation=90)

# set axs[0] yticks font size
axs[0].tick_params(axis='y', labelsize=16)

print("\n vdw     ti rigid")
bar_acc, bar_med, bar_high, bar_near_acc = extract_bars(bound_vdw_ti, ns)
print_formatted_list("bar_high     vdw_ti_rigid", bar_high)
print_formatted_list("bar_med      vdw_ti_rigid", bar_med)
print_formatted_list("bar_acc      vdw_ti_rigid", bar_acc)
print_formatted_list("bar_near_acc vdw_ti_rigid", bar_near_acc)

axs[1].bar(r, bar_near_acc, color = 'lightgray',
            width = width, edgecolor = 'black',
            label='Near acceptable (3 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 4 \mathrm{\\AA}$)')
axs[1].bar(r, bar_acc, color = '#a5cee2',
            width = width, edgecolor = 'black',
            label='Acceptable (2 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 3 \mathrm{\\AA}$)')
axs[1].bar(r, bar_med, color = '#b2df8a',
        width = width, edgecolor = 'black',
            label='Medium (1 $\mathrm{\\AA} < \mathrm{IL{-}RMSD} \leq 2 \mathrm{\\AA}$)')
axs[1].bar(r, bar_high, color = '#33a02b',
        width = width, edgecolor = 'black',
            label='High ($\mathrm{IL{-}RMSD} \leq 1 \mathrm{\\AA}$)')
axs[1].set_ylim((0,1.01))
# set x ticks
axs[1].set_xticks(r)
axs[1].set_xticklabels(tns, fontsize=16, rotation=90)


axs[1].set_yticks([])
lines_labels = [axs[1].get_legend_handles_labels()]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, fontsize=18, ncol=2, loc="lower center", bbox_to_anchor=(0.5, -0.10), bbox_transform=fig.transFigure)

axs[0].set_title("default scoring function", fontsize=20)
axs[1].set_title("vdW scoring function", fontsize=20)
axs[0].set_ylabel('Full dataset\n(89 complexes)', fontsize=20)


y_values = [0.2, 0.4, 0.6, 0.8]
for y in y_values:
    axs[0].axhline(y=y, color='black', linestyle='-', alpha=0.1, zorder=0)
    axs[1].axhline(y=y, color='black', linestyle='-', alpha=0.1, zorder=0)

# full title for the figure
#fig.suptitle("Bound docking", fontsize=24, y=1)
plt.subplots_adjust(top=0.90)

#plt.tight_layout()
plt.savefig("figures/SR_bound_overall_ti_def_vs_vdw.png", dpi=1200, bbox_inches="tight")
plt.close()

