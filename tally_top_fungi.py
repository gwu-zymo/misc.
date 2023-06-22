#tally up all the top fungal species in pbg samples
import os, sys

all = {}
for file in os.listdir('./'):
  if file.endswith('.zymo'):
    inp = open(f"{file}/{file}/midog.b.FungiITS/taxa_plots/sorted_out_L6.txt", 'r')
    line = inp.readline()
    line = inp.readline()
    ll = line.strip('\n').split('\t')
    for sample in ll[1:]:
      if (not 'Control' in sample) and (not 'Syn.' in sample) and (not 'Pos.' in sample) and (not 'Neg.' in sample):
        n = ll.index(sample)
    if not sample in all:
      all[sample] = ['', 0]
    line = inp.readline()
    while line:
      ll = line.strip('\n').split('\t')
      abd = float(ll[n])
      if abd > all[sample][1]:
        all[sample][1] = abd
        all[sample][0] = ll[0]
      line = inp.readline()
    inp.close()

for sample in all:
  print(f"{sample}\t{all[sample][0]}\t{all[sample][1]}")
