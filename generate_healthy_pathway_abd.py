#take the healthy species abundance and generate healthy pathway ranges
import os, sys

pathway_all = {}
pathway_abd = {}
inp = open('pathway.txt', 'r')
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  taxa = ll[0]
  pathway = ll[1]
  if not pathway in pathway_all:
    pathway_all[pathway] = []  
  pathway_all[pathway].append(taxa)
  line = inp.readline()
inp.close()

inp = open('Healthy_Gut_Cohort_Species_Taxa_V1.csv', 'r')
line = inp.readline()
line = inp.readline()
while line:
  ll = line.strip('\n').split(',')
  old_name = ll[0].split(';')[-1]
  g = old_name.split(' ')[0].lstrip('s__').split('_')[0]
  s = old_name.split(' ')[1].split('_')[0]
  name = f"{g} {s}"
  for pathway in pathway_all:
    if name in pathway_all[pathway] or g in pathway_all[pathway]:
      if pathway not in pathway_abd:
        pathway_abd[pathway] = list(map(float, ll[1:]))
      else:
        pathway_abd[pathway] = [x + y for x, y in zip(pathway_abd[pathway], list(map(float, ll[1:])))]
  line = inp.readline()
inp.close()

oup = open('Healthy_pathway.txt', 'w')
for pathway in pathway_abd:
  numbers = '\t'.join(list(map(str, pathway_abd[pathway])))
  oup.write(f"{pathway}\t{numbers}\n")
oup.close()





