#take the genus output of our pipeline and integrate into the enterotype data
#add a column to the 33 samples of the original data file
#need folder sample_ID; for example: pbg0530.230511.zymo 1235364

import os, sys

folder = sys.argv[1]
sample = sys.argv[2]

#get a list of genera involved in the analysis
genus_list = {}
inp = open('MetaHIT_SangerSamples.genus.txt', 'r')
line = inp.readline()
while line:
  genus = line.split('\t')[0]
  genus_list[genus] = [line.strip('\n'), 0]
  line = inp.readline()
inp.close()

genus_list[''][1] = sample

#parse sample file
inp = open(f"./{folder}/midog.a.Bac16Sv13/taxa_plots/sorted_otu_L6.txt", 'r')
total = 0
line = inp.readline()
line = inp.readline()
ll = line.strip('\n').split('\t')
sample_i = ll.index(sample)
line = inp.readline()
while line:  
  ll = line.strip('\n').split('\t')
  genus = ll[0].split(';')[-1].lstrip('g__').split('-')
  for key in genus:
    if key in genus_list: 
      genus_list[key][1]+=float(ll[sample_i])/len(genus)
      total+=float(ll[sample_i])/len(genus)
  line = inp.readline()
inp.close()

genus_list['-1'][1] = str(1 - total)

oup = open('sample_entero.data.txt', 'w')
for genus in genus_list:
  oup.write(genus_list[genus][0] + '\t' + str(genus_list[genus][1]) + '\n')
oup.close()
    
  
  
  
  
  
  
  
  
  
  
