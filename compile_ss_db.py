import os, sys

all = {}
inp = open('assembly_combined.txt', 'r')
line = inp.readline()
line = inp.readline()
while line:
  ll = line.split('\t')
  taxid = 'taxid_' + ll[6]
  spe = ll[7]
  all[taxid] = spe
  line = inp.readline()
inp.close()
  


inp = open('export_2023-02-24_20_42_12.499309.csv', 'r')
line = inp.readline()
line = inp.readline()
while line:
  ll = line.strip('\n').split(',')
  taxid = 'taxid_' + ll[1].strip('.txt').split('_')[-1]
  id = ll[0]
  try:
    os.system('mv %s %s' % (id, taxid))
  except:
    pass
  line = inp.readline()
inp.close()

oup = open('ssdb_2_28_2023.txt', 'w')
for file in os.listdir('./'):
  if file.startswith('taxid_'):
    inp = open('./%s/Cluster_Result/hclsMap_95.txt', 'r')
    gset = {}
    line = inp.readline()
    while line:
      ll = line.strip('\n').split('\t')
      for g in ll[-1].split(','):
        gset[g] = ''
    oup.write('%s\t%s\t%i\t%s\n' % (file, all[file], len(gset), ','.join(gset)))
oup.close()






'''
db_set = os.listdir('./')

all = {}
inp = open('ss_ref_db_10_2022.list', 'r')
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  if len(ll) > 2:
    spe = ll[2]
    taxid = ll[0]
    nr = ll[1]
    if ('taxid_' + taxid) in db_set:
      all[taxid] = [spe, nr]
  line = inp.readline()
inp.close()



for file in os.listdir('../run/'):
  taxid = file.split('.')[0].split('_')[2]
  if taxid in all:
    inp = open('../run/' + file, 'r')
    flist = []
    line = inp.readline()
    while line:
      flist.append(line.strip().replace('_genomic.fna', ''))
      line = inp.readline()
    inp.close()
    all[taxid].append(flist)
    
oup = open('ssdb_11_15_2022.txt', 'w')
oup2 = open('not_found', 'w')
for taxid in all:
  if len(all[taxid]) == 3:
    oup.write('%s\t%s\t%s\t11_15_2022\t%s\n' % (all[taxid][0], taxid, all[taxid][1], ','.join(all[taxid][2])))
  else:
    oup2.write('%s\t%s\t%s\n' % (all[taxid][0], taxid, all[taxid][1]))
oup.close()
oup2.close()
'''      
