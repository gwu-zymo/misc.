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

for file in os.listdir('../run/'):
  taxid = file.split('_')[2]
  if taxid in all:
    inp = open(file, 'r')
    flist = []
    line = inp.readline()
    while line:
      flist.append(line.strip().replace('_genomic.fna', ''))
      line = inp.readline()
    inp.close()
    all[taxid].append(flist)
    
oup = open('ssdb_11_15_2022.txt', 'r')
oup2 = open('not_found', 'w')
for taxid in all:
  if len(all[taxid]) == 3:
    oup.write('%s\t%s\t%s\t11_15_2022\t%s\n' % (all[taxid][0], taxid, all[taxid][1], ','.join(all[taxid][2])))
  else:
    oup2.write('%s\t%s\t%s\n' % (all[taxid][0], taxid, all[taxid][1]))
oup.close()
oup2.close()
      
