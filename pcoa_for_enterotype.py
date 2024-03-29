#generate pcoa plot for our sample's eneterotype
#need entero genus table and type prediction table
import os, sys
import pandas as pd
import numpy as np

data = pd.read_csv(sys.argv[1], sep='\t', index_col=0)
data = data[1:]
data = data.T

#scikit-learn
from sklearn.decomposition import PCA

pca = PCA(n_components=2)  # Set the desired number of components
pcoa = pca.fit_transform(data)

inp = open('entero.out', 'r')
line = inp.readline()
ll = line.strip('\n').split('\t')[1].split('|')[1:]
groups = [pair.split(',')[1] for pair in ll]
groups[-1] = '4'

import matplotlib.pyplot as plt

group_colors = ['pink', 'orange', 'blue', 'green']

plt.figure(figsize=(8, 6))  # Adjust the figure size as per your preference

for i, group in enumerate(set(groups)):
    group_samples = pcoa[np.array(groups) == group]
    if len(group_samples) > 0:
        plt.scatter(group_samples[:, 0], group_samples[:, 1], color=group_colors[i], label=f'Group {group}')

plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCoA Plot')
plt.legend(groups)

# highlight the last sample 
highlight_sample = pcoa[-1]
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
