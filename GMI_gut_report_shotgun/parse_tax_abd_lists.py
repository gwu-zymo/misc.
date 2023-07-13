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
  long_name = ll[0].split(';')[-1]
  g = long_name.split(' ')[0].lstrip('s__').split('_')[0]
  s = long_name.split(' ')[1].split('_')[0]
  species_name = f"{g} {s}"
  if not species_name in fungi_abd:
    fungi_abd[species_name] = 0
  fungi_abd[species_name]+=float(ll[pos])
  line = inp.readline()
inp.close()

oup = open(f"top_10_fun_{sample}.txt", 'w')
sorted_items = sorted(fungi_abd.items(), key=lambda x: x[1], reverse=True)[:10]
for key in sorted_items:
  if key[1] > 0 and (key[0] != 'Other Other') and (key[0] != 'NA NA'):
    oup.write(f"{key[0]}\t{key[1]}\n")
oup.close()

phylum_abd = {}
inp = open(f"./{folder}/00...AllSamples.illumina.pe/Prokaryote/AbundanceTables/2.Phylum/phylum.tsv", 'r')
line = inp.readline()
line = inp.readline()
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  phylum_name = ll[0].split(';')[-1].replace('p__', '').split('_')[0]
  if not phylum_name in phylum_abd:
    phylum_abd[phylum_name] = 0
  phylum_abd[phylum_name]+=float(ll[pos])
  line = inp.readline()
inp.close()

import matplotlib.pyplot as plt

def create_barplot(numbers, ratio, filename, label1, label2, color1, color2):
    labels = ['healthy median', '', 'you', '']
    x = [0.9, 1.5, 3, 3.6]  # Adjust the x-coordinates
    colors = [color1, color2, color1, color2]
    bar_data = list(zip(numbers, labels, x, colors))
    bar_data.sort(reverse=True)  # Sort the bar data based on the numbers
    
    sorted_numbers, sorted_labels, sorted_x, sorted_colors = zip(*bar_data)
    sorted_numbers = list(sorted_numbers)
    sorted_labels = list(sorted_labels)
    sorted_x = list(sorted_x)
    sorted_colors = list(sorted_colors)

    plt.bar(sorted_x, sorted_numbers, color=sorted_colors)
    plt.xlabel('')
    plt.ylabel('relative abundance')
    plt.title(ratio)

    x_l = [1.2, 1.2001, 3.3, 3.3001]
    plt.xticks(x_l, labels)
    
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=color1, label=label1),
        plt.Rectangle((0, 0), 1, 1, color=color2, label=label2)
    ]
    
    plt.legend(handles=legend_handles)
    plt.savefig(filename, transparent=True)
    plt.show()

    print(sorted_numbers)
    print(sorted_colors)

oup = open(f"{sample}_ratios.txt", 'w')
try:
  ratio_1 = phylum_abd['Firmicutes']/phylum_abd['Bacteroidota']
  name = 'Firmicutes_Bacteroidota'
  oup.write(f"{name}\t{ratio_1}\n")
  
  color1 = 'blue'
  label1 = 'Firmicutes'
  color2 = 'orange'
  label2 = 'Bacteroidetes'
  filename = f"{sample}_f-b_o.png"
  ratio = 'firmicutes/bacteroidetes ratio'
  numbers = [0.585, 0.351, phylum_abd['Firmicutes'], phylum_abd['Bacteroidota']]  # Replace with your two numbers
  create_barplot(numbers, ratio, filename, label1, label2, color1, color2)
  plt.clf()

except:
  pass
try:
  ratio_2 = phylum_abd['Proteobacteria']/phylum_abd['Actinobacteriota']
  name = 'Proteobacteria_Actinobacteriota'
  oup.write(f"{name}\t{ratio_2}\n")

  color1 = 'green'
  label1 = 'Proteobacteria'
  color2 = 'yellow'
  label2 = 'Actinobacteriota'
  filename = f"{sample}_p-a_o.png"
  ratio = 'proteobacteria/actinobacteriota ratio'
  numbers = [0.00858, 0.0168, phylum_abd['Proteobacteria'], phylum_abd['Actinobacteriota']]  # Replace with your two numbers
  create_barplot(numbers, ratio, filename, label1, label2, color1, color2)

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
  pathogen_list[species] = ''
  line = inp.readline()
inp.close()

oup = open(f"pathogen_{sample}.txt", 'w')
for species in species_abd:
  if species in pathogen_list:
    if species_abd[species] > 0:
      oup.write(f"{species}\t{species_abd[species]}\n")
oup.close()



