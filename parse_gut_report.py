#parse gut reports and find taxa present
#start with all the qiime analysis zip files stored in one folder
#multiple analysis zip files from the same sample is ok

import os, sys

all = {}
for file in os.listdir('./'):
  print('processing %s.......' % file)
  os.system('unzip %s' % file)
  folder = file.rstrip('.zip')
  if '.DIG' in folder:
    folder = folder.replace('.DIG', '.zymo')
  for pool in os.listdir('./%s/' % folder):
    if pool.startswith('midog.'):
      if not pool in all:
        all[pool] = {}
      try:  
        inp = open('./%s/%s/taxa_plots/sorted_otu_L7.txt' % (folder, pool))
        line = inp.readline()
        while line:
          if not line.startswith('#'):
            line_split = line.strip().split()
            taxa = line_split[0]
            if not taxa in all[pool]:
              all[pool][taxa] = 0
            all[pool][taxa]+=1
          line = inp.readline()
        inp.close()
      except:
        pass
  os.system('rm -r %s' % folder)
  
for pool in all:
  oup = open(pool + '_tally.txt', 'w')
  for taxa in all[pool]:
    oup.write('%s\t%i\n' % (taxa, all[pool][taxa]))
  oup.close()
          
  
