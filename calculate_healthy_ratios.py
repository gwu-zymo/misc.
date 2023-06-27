#calculate the healthy range of phylum/genus ratios from healthy abundance table

phylum_all = {}
genus_all = {}

inp = open('Healthy_Gut_Cohort_Species_Taxa_V1.csv', 'r')
line = inp.readline()
line = inp.readline()
while line:
  ll = line.strip('\n').split(',')
  phylum = ll[0].split(';')[1].lstrip('p__')
  genus = ll[0].split(';')[-2].lstrip('g__')
  if not phylum in phylum_all:
    phylum_all[phylum] = list(map(float, ll[1:]))
  else:
    phylum_all[phylum] = [x + y for x, y in zip(phylum_all[phylum], list(map(float, ll[1:])))]
  if not genus in genus_all:
    genus_all[genus] = list(map(float, ll[1:]))
  else:
    genus_all[genus] = [x + y for x, y in zip(genus_all[genus], list(map(float, ll[1:])))]
  line = inp.readline()
inp.close()

for phylum in phylum_all:
  for i in range(0, len(phylum_all[phylum])):
    phylum_all[phylum][i]+=0.00000000000000000001
for genus in genus_all:
  for i in range(0, len(genus_all[genus])):
    genus_all[genus][i]+=0.00000000000000000001


oup = open('healthy_ratios.txt', 'w')
ratios = [x/y for x, y in zip(phylum_all['Firmicutes'], phylum_all['Bacteroidota'])]
ratios_w = '\t'.join(list(map(str, ratios)))
oup.write(f"Firmicutes|Bacteroidota\t{ratios_w}\n")
ratios = [x/y for x, y in zip(phylum_all['Proteobacteria'], phylum_all['Actinobacteriota'])]
ratios_w = '\t'.join(list(map(str, ratios)))
oup.write(f"Proteobacteria|Actinobacteriota\t{ratios_w}\n")
ratios = [x/y for x, y in zip(genus_all['Prevotella'], genus_all['Bacteroides'])]
ratios_w = '\t'.join(list(map(str, ratios)))
oup.write(f"Prevotella|Bacteroides\t{ratios_w}\n")
oup.close()
