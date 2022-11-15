import os, sys

all = {}
inp = open('ss_ref_db_10_2022.list', 'r')
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  spe = ll[2]
  taxid = ll[0]
  nr = ll[1]
  all[taxid] = [spe, nr]
  line = inp.readline()
inp.close()

inp = open('ssdb_202211100824.csv.csv', 'r')
line = inp.readline()
while line:
  ll = line.strip('\n').split(',')
  taxid = 'taxid_' + ll[1].split('_')[-1]
  id = ll[0]
  for file in os.listdir('./'):
    if file == id:
      os.system('mv %s %s' % (id, taxid))
  line = inp.readline()
inp.close()

