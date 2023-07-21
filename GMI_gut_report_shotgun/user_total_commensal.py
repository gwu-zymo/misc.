import pandas as pd
import numpy as np
import matplotlib.pyplot as mp
import sys

#command: python3 runID sampleID
folder = sys.argv[1]
SampleID = sys.argv[2]


Total_commensal_abd = pd.read_csv('./%s/00...AllSamples.illumina.pe/All/AbundanceTables/1.Superkingdom/superkingdom.tsv' % folder, skiprows = 1, sep='\t')
Total_commensal_abd['#OTU ID'] = Total_commensal_abd['#OTU ID'].str[3:]


superkdict = {}
superkdict = Total_commensal_abd.set_index('#OTU ID')[SampleID].to_dict()
#print(superkdict)

superklen = len(superkdict)
#print(superklen)

d1 = 0
d2 = 0
d3 = 0
d4 = 0
sample = [1]
Metrics = list(superkdict.keys())
#print(Metrics)
for item in Metrics:
    if 'Archaea' == item:
        d1 = superkdict[item]
    elif 'Bacteria' == item:
        d2 = superkdict[item]
    elif 'Eukaryota' == item:
        d3 = superkdict[item]
    elif 'Viruses' == item:
        d4 = superkdict[item]
    else:
        continue
#print(d1,d2,d3,d4)

#ax = mp.subplots(figsize=(15,1))
mp.rcParams["figure.figsize"] = [17.5,1]
bar1 = mp.barh(sample, superkdict['Archaea'], color = "red")
bar2 = mp.barh(sample, superkdict['Bacteria'], left=superkdict['Archaea'], color = "blue")
bar3 = mp.barh(sample, superkdict['Eukaryota'], left=superkdict['Archaea'], color = "green")
bar4 = mp.barh(sample, superkdict['Viruses'], left=superkdict['Archaea'], color = "black")
mp.yticks([])
mp.xticks([])
mp.legend(Metrics,fontsize="large",bbox_to_anchor=(0.95,1.6),loc='upper right',ncol=len(Metrics))
mp.margins(0,0)
mp.savefig('%s_Total_Commensal.png' % SampleID,bbox_inches='tight',transparent=True)
#mp.show()
