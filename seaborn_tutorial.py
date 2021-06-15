# %%

import os
import re
import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

print("Seaborn version : ", sns.__version__)
sns.set()
sns.set_style('darkgrid')
penguins = sns.load_dataset('penguins')
#sns.histplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
#sns.despine(left=True, bottom=True)



# %%
"""
sns.kdeplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
# %%
sns.displot(data=penguins, x="flipper_length_mm", hue="species", col="species")
# %%
f, axs = plt.subplots(1, 2, figsize=(8, 4), gridspec_kw=dict(width_ratios=[4, 3]))
sns.scatterplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species", ax=axs[0])
sns.histplot(data=penguins, x="species", hue="species", shrink=.8, alpha=.8, legend=False, ax=axs[1])
f.tight_layout()
# %%
tips = sns.load_dataset("tips")
g = sns.relplot(data=tips, x="total_bill", y="tip")
g.ax.axline(xy1=(10, 2), slope=.2, color="b", dashes=(5, 2))
# %%
f1, ax1 = plt.subplots()
f2, ax2 = plt.subplots(1, 2, sharey=True)
# %%
g = sns.FacetGrid(penguins)
# %%
g = sns.FacetGrid(penguins, col="sex", height=3.5, aspect=.75)
# %%
sns.jointplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species")
# %%
sns.pairplot(data=penguins, hue="species")
# %%
sns.jointplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species", kind="hist")
# %%
sns.pairplot(data=penguins, hue="species", kind="hist")


"""
# %%
flights = sns.load_dataset("flights")

"""
sns.set_color_codes()
current_palette = sns.color_palette()
sns.palplot(current_palette)
sns1 = sns.relplot(data=flights, x="year", y="passengers", hue="month", kind="line")
sns.despine(left=True, bottom=True)
plt.show()

flights_wide = flights.pivot(index="year", columns="month", values="passengers")
print(flights_wide.head())
sns.relplot(data=flights_wide, kind="line")
"""
# %%
flight_avg = flights.groupby(["year"]).mean()


flights_wide = flights.pivot(index="year", columns="month", values="passengers")

two_series = [flights_wide.loc[:1955, "Jan"], flights_wide.loc[1952:, "Aug"]]
sns.relplot(data=two_series, kind="line")
plt.show()