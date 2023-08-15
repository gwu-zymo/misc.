#add up multiple lines of the same phylum

phylum_abd = {}
inp = open('phylum.tsv', 'r')
line = inp.readline()
line = inp.readline()
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  phylum_name = ll[0].split(';')[-1].replace('p__', '').split('_')[0]
  if not phylum_name in phylum_abd:
    phylum_abd[phylum_name] = []
  values = [float(x) for x in ll[1:]]
  phylum_abd[phylum_name] = [x + y for x, y in zip(phylum_abd[phylum_name], values)]
  line = inp.readline()
inp.close()
