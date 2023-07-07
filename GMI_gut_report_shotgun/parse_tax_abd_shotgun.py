#parse the sample species and genus abundance tables and prepare species list abundance tables for shotgun sourmash output
#keystone list, pathogen list, pathway list, phylum ratios
#use: python3 parse_tax_abd_lists.py folder sample_ID; for example: in3773.230505 1BW	
import os, sys

folder = sys.argv[1]
sample = sys.argv[2]
species_abd = {}
inp = open(f"./{folder}/00...AllSamples.illumina.pe/Prokaryote/AbundanceTables/6.Species/species.tsv", 'r')
line = inp.readline()
line = inp.readline()
ll = line.strip('\n').split('\t')
pos = ll.index(sample)
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  long_name = ll[0].split(';')[-1]
  g = long_name.split(' ')[0].lstrip('s__').split('_')[0]
  s = long_name.split(' ')[1].split('_')[0]
  species_name = f"{g} {s}"
  if not species_name in species_abd:
    species_abd[species_name] = 0
  species_abd[species_name]+=float(ll[pos])
  line = inp.readline()
inp.close()

genus_abd = {}
inp = open(f"./{folder}/00...AllSamples.illumina.pe/Prokaryote/AbundanceTables/5.Genus/genus.tsv", 'r')
line = inp.readline()
line = inp.readline()
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  genus_name = ll[0].split(';')[-1].replace('g__', '').split('_')[0]
  if not genus_name in genus_abd:
    genus_abd[genus_name] = 0
  genus_abd[genus_name]+=float(ll[pos])
  line = inp.readline()
inp.close()

inp = open('keystone.txt', 'r')
oup = open(f"keystone_{sample}.txt", 'w')
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
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
      oup.write(f"{line.strip()}\t0\n")
  else:
    if name in genus_abd:
      oup.write(f"{line.strip()}\t{genus_abd[name]}\n")
      all_path[pathway]+=float(genus_abd[name])
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
inp = open(f"./{folder}/00...AllSamples.illumina.pe/Eukaryote/AbundanceTables/6.Species/species.tsv", 'r')
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





