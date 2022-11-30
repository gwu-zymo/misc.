# download genomes

import os, sys

inp = open('core_set_562_modified.txt', 'r')
all = {}
line = inp.readline()
while line:
  key = line.strip('\n').replace('_genomic.fna', '')
  all[key] = ''
  line = inp.readline()
inp.close()

inp = open('assembly_summary_genbank.txt', 'r')
line = inp.readline()
while line:
  for key in all:
    if key in line:
      path = line.split('\t')[19]
      fpath = '%s/%s_genomic.fna.gz' % (path, key)
      print(fpath)
      os.system('wget %s' % fpath)
      break
  line = inp.readline()
inp.close()
