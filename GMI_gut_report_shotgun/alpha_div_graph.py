import pandas as pd
import numpy as np
import matplotlib.pyplot as mp
import statistics
import sys

#command: python3 {script} runID sampleID
folder = sys.argv[1]
SampleID = sys.argv[2]

AlphaDivMedian = 229
AlphaDivSample = 0

sample_species_count = pd.read_csv('./%s/00...AllSamples.illumina.pe/Prokaryote/AlphaDiversity/6.Species/ObservedSp.csv' % folder)
#print(sample_species_count)

AlphaDivSample = sample_species_count.columns[1]
print(AlphaDivSample)
xax = ['Your Sample', 'Healthy Sample']
yax = [int(AlphaDivSample), int(AlphaDivMedian)]

mp.figure(figsize=(10,5))
mp.bar(xax, yax, color = ['blue', 'orange'])
mp.savefig('%s_model_Alpha_Div.png' % SampleID, bbox_inches='tight', transparent=True)
#mp.show
