#transform rgi_amr_out.txt to a list of species with top AMR genes in each of them

import operator

#all[species] = {amr1: 0.9, amr2: 0.8}
all = {}

inp = open('rgi_amr_out.txt', 'r')
line = inp.readline()
while line:
    ll = line.strip('\n').strip('\t').split('\t')
    amr = ll[0]
    for key in ll[1:]:
        s_key = key.split('|')
        spe = s_key[0]
        pct = float(s_key[1])
        ct = s_key[2]
        spe_c = spe + '|' + ct
        if not spe_c in all:
            all[spe_c] = {}
        all[spe_c][amr] = pct
    line = inp.readline()
inp.close()

oup = open('spe_amr_list.txt', 'w')
for spe in all:
    oup.write('%s\t' % spe)
    sorted_amr = sorted(all[spe].items(), key=operator.itemgetter(1), reverse=True)
    for amr in sorted_amr:
        oup.write('%s|%f\t' % (amr[0], amr[1]))
    oup.write('\n')
oup.close()
