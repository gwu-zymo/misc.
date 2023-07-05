#parse the sample species and genus abundance tables and prepare species list abundance tables
#keystone list, pathogen list, pathway list, phylum ratios
#use: python3 parse_tax_abd_lists.py folder sample_ID; for example: pbg0530.230511.zymo 1235364	
import os, sys

folder = sys.argv[1]
sample = sys.argv[2]
species_abd = {}
inp = open(f"./{folder}/midog.a.Bac16Sv13/taxa_plots/sorted_otu_L7.txt", 'r')
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
    species_name = ' '.join(ll[0].split(';')[-2:len(ll)+1]).replace('g__', '').replace('s__', '')
  species_abd[species_name] = float(ll[pos])
  line = inp.readline()
inp.close()

genus_abd = {}
inp = open(f"./{folder}/midog.a.Bac16Sv13/taxa_plots/sorted_otu_L6.txt", 'r')
line = inp.readline()
line = inp.readline()
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  genus_name = ll[0].split(';')[-1].replace('g__', '')
  genus_abd[genus_name] = float(ll[pos])
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
      all_path[pathway]+=species_abd[name]
    else:
      oup.write(f"{line.strip()}\t0\n")
  else:
    if name in genus_abd:
      oup.write(f"{line.strip()}\t{genus_abd[name]}\n")
      all_path[pathway]+=genus_abd[name]
    else:
      oup.write(f"{line.strip()}\t0\n")
  line = inp.readline()
inp.close()
oup.close()
oup = open(f"pathway_compiled_{sample}.txt", 'w')  
for pathway in all_path:
  oup.write(f"{pathway}\t{all_path[pathway]}\n")
oup.close()
            
oup = open(f"top_10_bac_{sample}.txt", 'w')
sorted_items = sorted(species_abd.items(), key=lambda x: x[1], reverse=True)[:10]
for key in sorted_items:
  oup.write(f"{key[0]}\t{key[1]}\n")
oup.close()

fungi_abd = {}
inp = open(f"./{folder}/midog.b.FungiITS/taxa_plots/sorted_otu_L7.txt", 'r')
line = inp.readline()
line = inp.readline()
ll = line.strip('\n').split('\t')
pos = ll.index(sample)
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  species_name = ' '.join(ll[0].split(';')[-2:len(ll)+1]).replace('g__', '').replace('s__', '')
  fungi_abd[species_name] = float(ll[pos])
  line = inp.readline()
inp.close()

oup = open(f"top_10_fun_{sample}.txt", 'w')
sorted_items = sorted(fungi_abd.items(), key=lambda x: x[1], reverse=True)[:10]
for key in sorted_items:
  if key[1] > 0 and (key[0] != 'Other Other') and (key[0] != 'NA NA'):
    oup.write(f"{key[0]}\t{key[1]}\n")
oup.close()

phylum_abd = {}
inp = open(f"./{folder}/midog.a.Bac16Sv13/taxa_plots/sorted_otu_L2.txt", 'r')
line = inp.readline()
line = inp.readline()
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  phylum_name = ll[0].split(';')[-1].replace('p__', '')
  phylum_abd[phylum_name] = float(ll[pos])
  line = inp.readline()
inp.close()

oup = open(f"{sample}_ratios.txt", 'w')
try:
  ratio_1 = phylum_abd['Firmicutes']/phylum_abd['Bacteroidetes']
  name = 'Firmicutes_Bacteroidota'
  oup.write(f"{name}\t{ratio_1}\n")
except:
  pass
try:
  ratio_2 = phylum_abd['Proteobacteria']/phylum_abd['Actinobacteria']
  name = 'Proteobacteria_Actinobacteriota'
  oup.write(f"{name}\t{ratio_2}\n")
except:
  pass
try:
  ratio_3 = genus_abd['Prevotella']/genus_abd['Bacteroides']
  name = 'Prevotella_Bacteroides'
  oup.write(f"{name}\t{ratio_3}\n")
except:
  pass
oup.close() 

inp = open('pathogen.txt', 'r')
pathogen_list = {}
line = inp.readline()
while line:
  species = line.strip('\n').split('\t')[0].strip()
  genus =  species.split(' ')[0]
  pathogen_list[genus] = ''
  line = inp.readline()
inp.close()

oup = open(f"pathogen_{sample}.txt", 'w')
for species in species_abd:
  genus = species.split(' ')[0]
  if genus in pathogen_list:
    if species_abd[species] > 0:
      oup.write(f"{species}\t{species_abd[species]}\n")
oup.close()


