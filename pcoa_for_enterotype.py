#generate pcoa plot for our sample's eneterotype
#need entero genus table and type prediction table
import os, sys
import pandas as pd

data = pd.read_csv(sys.argv[1], sep='\t', index_col=0)
data = data[1:]

from sklearn.decomposition import PCA

pca = PCA(n_components=2)  # Set the desired number of components
pcoa = pca.fit_transform(data)

groups = ['Group1', 'Group2', 'Group3'] * 11

import matplotlib.pyplot as plt

group_colors = ['red', 'green', 'blue']  # Colors for the three groups

plt.figure(figsize=(8, 6))  # Adjust the figure size as per your preference

for group, color in zip(groups, group_colors):
    group_samples = pcoa[groups == group]
    plt.scatter(group_samples[:, 0], group_samples[:, 1], color=color)

plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCoA Plot')
plt.legend(groups)

# Assuming you want to highlight a sample with index 'highlight_idx'
highlight_sample = pcoa[highlight_idx]
plt.scatter(highlight_sample[0], highlight_sample[1], color='black', marker='*', s=100)

plt.show()

import numpy as np

# Calculate the convex hull for each group
convex_hulls = []
for group in groups:
    group_samples = pcoa[groups == group]
    convex_hull = np.vstack((group_samples, group_samples[0]))  # Closing the convex hull
    convex_hulls.append(convex_hull)

# Plot the convex hulls for each group
for convex_hull, color in zip(convex_hulls, group_colors):
    plt.fill(convex_hull[:, 0], convex_hull[:, 1], color=color, alpha=0.2)

plt.savefig('pcoa_plot.png')
