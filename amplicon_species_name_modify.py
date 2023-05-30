#take in amplicon seq taxonomy table, modify the genus/species names to adress species complex names
#convert species complex names to standard binomial species names
#all combinations of names are considered and abundance is transferred to all of them
#in any of the functional lists, it is unlikely that two species from the same species complex are present

import os, sys

inp = open(sys.argv[1], 'r')
oup = open(sys.argv[1] + '.mod', 'w')
line = inp.readline()
while line:
  if line.startswith('#'):
    oup.write(line)
  else:
    line_split = line.strip('\n').split('\t')
    abundance = '\t'.join(line_split[1:]) + '\n'
    full_name = line_split([0])
    split_name = full_name.split(';')
    genus = split_name[-2].strip('g__').split('-')
    species = split_name[-1].strip('s__').split('-')
    for g in genus:
      for s in species:
        oup.write('%s_%s\t%s' % (g, s, abundance))
  line = inp.readline()
inp.close()
oup.close()
        
        
        
        
