import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
short = []
ll = []
lb = []

rmsd_file = Path("..", "data", "RMSD_glycam_to_bound.txt")
with open(rmsd_file, "r") as r:
    for ln in r:
        if ln.startswith("short") == True:
            continue
        splt_ln = ln.split()
        short.append(float(splt_ln[0]))
        if len(splt_ln) > 1:
            ll.append(float(splt_ln[1]))
        if len(splt_ln) > 2:
            lb.append(float(splt_ln[2]))

data = [short, ll, lb]
fig, ax = plt.subplots()
colors = ['blue', 'red', 'green']
plots = ax.violinplot(data, showmeans=True, showextrema=False)
plots['cmeans'].set_colors("black")
# Set the color of the violin patches
for pc, color in zip(plots['bodies'], colors):
    pc.set_facecolor(color)
means = [np.mean(short), np.mean(ll), np.mean(lb)]
maxes = [np.max(short), np.max(ll), np.max(lb)]
mins = [np.min(short), np.min(ll), np.min(lb)]

# let's extract the 75 percentile values from the violin plots
percent_75 = [np.percentile(short, 75), np.percentile(ll, 75), np.percentile(lb, 75)]
# let's extract the 25 percentile values from the violin plots
percent_25 = [np.percentile(short, 25), np.percentile(ll, 25), np.percentile(lb, 25)]

#medians = [median.get_ydata()[0] for median in plots['cmedians']]
for i, mean in enumerate(means):
    ax.text(i + 1, mean+0.01, f'${mean:.2f}\ \AA$', ha='center', va='bottom', color='black', fontsize=12)
for i, max_ in enumerate(maxes):
    ax.text(i + 1, max_-0.05, f'${max_:.2f}\ \AA$', ha='center', va='bottom', color='black', fontsize=12)
for i, min_ in enumerate(mins):
    ax.text(i + 1, min_+0.01, f'${min_:.2f}\ \AA$', ha='center', va='bottom', color='black', fontsize=12)

#ax.set_title('Glycan RMSD distribution', fontsize=16)
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(['short\n(S)', 'long-linear\n(LL)', 'long-branched\n(LB)'], fontsize=15)
ax.set_ylabel("RMSD ($\AA$)", fontsize=16)
ax.set_ylim(0, 3.8)
plt.tight_layout()
plt.savefig(Path("figures", "glycan-rmsd-violin.png"), dpi=300)
