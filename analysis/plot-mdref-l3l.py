import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import argparse
import numpy as np

parse = argparse.ArgumentParser(description="Makes histogram in .png format")
parse.add_argument("figname", help = "Provide name for the figure")
args = parse.parse_args()

data = pd.read_csv('../data/mdref-l3l.tsv', delimiter='\t')

# Use only columns starting from the second one
data = data.iloc[:, 1:]

print(data)

# Check if the data is empty after handling missing values
if data.empty:
    print("No valid data to plot.")
else:
    plt.figure(figsize=(7, 5))
    colors = ["#224fdf", "#df7d20", "#30b346", "#cb1d25", "#dc61b8", "#a3a3a3"]

    # Melt the DataFrame into a long format
    melted_data = data.melt(var_name='variables', value_name='values')
#    print(melted_data)

    # Compute the average
    ave = melted_data.groupby(['variables'])['values'].mean()

    # Create the boxplot, with the variable names as the x-axis and different colors for each variable
    ax = sns.boxplot(
        x='variables', y='values', data=melted_data, palette=colors, orient="v", width=0.5, showmeans=True,
        meanprops={"marker": "o", "markerfacecolor": "white", "markeredgecolor": "black", "markersize": "4"},
        medianprops={"visible": False}
    )

    # Get the x-axis labels (categories)
    categories = ax.get_xticklabels()

    # Add average values on top of the box plots
    for i, category in enumerate(categories):
        ax.text(i, ave[category.get_text()] + 0.03, round(ave[category.get_text()], 2),
                horizontalalignment='center', size='small', color='white', weight='semibold')

    plt.yticks(fontsize=9)
    plt.xticks(fontsize=9)  
    plt.ylabel("RMSD ($\mathrm{\AA}$)", fontsize=9)
    plt.xlabel(" ")
    plt.ylim(0.0, 4.0)
    [plt.axhline(y=i, color="grey", linestyle="dotted") for i in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]]

    true_title = "long linear (LL) glycans"
    plt.title(true_title, fontsize=10)

# savefig
figname=args.figname
# Define the path to the figures directory
figures_dir = os.path.join(os.getcwd(), "figures")
# Construct the full path for the figure file
fig_path = os.path.join(figures_dir, figname + ".png")
plt.tight_layout()
plt.savefig(fig_path, transparent=False, dpi=600)
