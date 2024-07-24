# Import the necessary libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import argparse
from adjustText import adjust_text


parse = argparse.ArgumentParser(description = "Makes histogram in .png format")
parse.add_argument("figname", help = "Provide name for the figure")
args = parse.parse_args()


# Load the data into a pandas DataFrame
df = pd.read_csv('../data/SL-SB-scatter.tsv', delimiter='\t')

# Create a scatter plot
plt.figure(figsize=(8, 8))

colors=["darkblue"]
legend_labels = [("SL-SB glycans")]

ax = sns.scatterplot(data=df, x='lowest-RSMD-to-REF', y='lowest-RMSD-to-REF-after-clustering', hue='group', palette=colors, legend=False)

# Create a list to store the text objects
texts = []
for i, point in df.iterrows():
    texts.append(ax.text(point['lowest-RSMD-to-REF'], point['lowest-RMSD-to-REF-after-clustering'], point['name']))

# Use adjust_text to automatically position the text annotations
adjust_text(texts)


# Create a list of Patch objects for the legend
from matplotlib.patches import Patch
legend_patches = [Patch(facecolor=c, label=l) for c, l in zip(colors, legend_labels)]

# Add the custom legend to the plot
plt.legend(handles=legend_patches, loc="lower right", fontsize=14)


plt.xlim(0.0, 1.6)
plt.ylim(0.0, 1.6)


x = np.linspace(*plt.xlim()) 
plt.plot(x, x, color='gray') 

# Adding minor ticks
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

# Adding grid
ax.grid(which='both', alpha=0.4, linestyle='dashed', linewidth=0.2, color='gray')
ax.grid(which='minor', alpha=0.4)



plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14) 
plt.xlabel("lowest RMSD overall sampling ($\mathrm{\AA}$)", fontsize = 14)
plt.ylabel("lowest RMSD after clustering ($\mathrm{\AA}$)", fontsize = 14)

# savefig
figname=args.figname
# Define the path to the figures directory
figures_dir = os.path.join(os.getcwd(), "figures")
# Construct the full path for the figure file
fig_path = os.path.join(figures_dir, figname + ".png")
plt.tight_layout()
plt.savefig(fig_path, transparent=False, dpi=600)

