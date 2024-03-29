import pandas as pd
import numpy as np
import matplotlib.pyplot as mp
import sys


#command: python3 runID sampleID
folder = sys.argv[1]
SampleID = sys.argv[2]

HealthyScoreTaxa = pd.read_csv("HealthySpeciesOfInterest.csv")
#print(HealthyScoreTaxa)

UserData = pd.read_csv("./%s/00...AllSamples.illumina.pe/Prokaryote/AbundanceTables/6.Species/species.tsv" % folder, sep = '\t', skiprows = 1 )
#UserData = UserData.tail(-1)
print(UserData)

maxscore = 250
compositescore = maxscore
taxadict = {}

taxadict = UserData.set_index('#OTU ID')[SampleID].to_dict()
#print(taxadict)


for key in taxadict:
    for index, row in HealthyScoreTaxa.iterrows():
        i = 0
        if key == row[0]:
            #print('Match')
            if taxadict[key] <= row[1]:
                i = -2
            elif taxadict[key] <= row [2]:
                i = -1
            elif taxadict[key] >= row [4]:
                i = -2
            elif taxadict[key] >= row [5]:
                i = 1
            else:
                i = -0.25
            compositescore = compositescore + i
            #print(compositescore)

        #else:
            #print('no match')
oup = open('%s_HealthScore.csv' % SampleID, 'w')
oup.write(str(compositescore))
oup.close()
