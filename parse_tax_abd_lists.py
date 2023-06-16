#parse the sample species and genus abundance tables and prepare species list abundance tables
#keystone list, pathogen list, pathway list, phylum ratios
#use: python3 parse_tax_abd_lists.py folder sample_ID; for example: pbg0530.230511.zymo 1235364	
import os, sys

folder = sys.argv[1]
sample = sys.argv[2]
species_abd = {}
inp = open(f"/{folder}/midog.a.Bac16Sv13/taxa_plots/sorted_otu_L7.txt", 'r')
line = inp.readline()
line = inp.readline()
ll = line.strip('\n').split('\t')
pos = ll.index(sample)
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  if 'f_Christensenellaceae;g__NA;s__NA' in line:
    species_name = 'Christensenellaceae NA'
  else:
    species_name = ' '.join(ll[0].split(';')[-2:len(ll)]).replace('g__', '').replace('s__', '')
  species_abd[species_name] = ll[pos]
  line = inp.readline()
inp.close()

genus_abd = {}
inp = open(f"/{folder}/midog.a.Bac16Sv13/taxa_plots/sorted_otu_L6.txt", 'r')
line = inp.readline()
line = inp.readline()
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  genus_name = ll[0].split(';')[-1].replace('g__', '')
  genus_abd[genus_name] = ll[pos]
  line = inp.readline()
inp.close()

inp = open('keystone.txt', 'r')
oup = open(f"keystone_{sample}.txt", 'w')
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  if len(ll) == 2:
    name_na = ll[1]
    name = ll[0]
    if name_na in species_abd:
      oup.write(f"{name}\t{species_abd[name_na]}\n")
    else:
      oup.write(f"{name}\t0\n")
  elif len(ll) == 1:
    name = ll[0]
    if name in species_abd:
      oup.write(f"{name}\t{species_abd[name]}\n")
    else:
      oup.write(f"{name}\t0\n")
  line = inp.readline()
inp.close()
oup.close()

inp = open('pathway.txt', 'r')
oup = open(f"pathway_{sample}.txt", 'w')
all_path = {}
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  name = ll[0]
  pathway = ll[1]
  if not pathway in all_path:
    all_path[pathway] = 0
  if ' ' in name:
    if name in species_abd:
      oup.write(f"{line.strip()}\t{species_abd[name]}\n")
      all_path[pathway]+=float(species_abd[name])
    else:
      oup.write(f"{line.strip('\n')}\t0\n")
  else:
    if name in genus_abd:
      oup.write(f"{line.strip()}\t{genus_abd[name]}\n")
      all_path[pathway]+=float(genus_abd[name])
    else:
      oup.write(f"{line.strip()}\t0\n")
  line = inp.readline()
inp.close()
oup.close()
oup = open(f"pathway_complied_{sample}.txt", 'w')  
for pathway in all_path:
  oup.write(f"{pathway}\t{all_path[pathway]}\n")
oup.close()
            
           
                




