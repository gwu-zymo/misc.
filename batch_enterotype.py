#batch run enterotyping r script
import os, sys, subprocess

oup = open('entero.out', 'w')
for zip in os.listdir('./'):
  if zip.endswith('.zip'):
    subprocess.run(['unzip', zip])
    folder = zip.rstrip('.zip')
    subprocess.run(['cp', './%s/midog.a.Bac16Sv13/taxa_plots/sorted_otu_L6.txt' % folder, '.'])
    inp = open('sorted_otu_L6.txt', 'r')
    line = inp.readline()
    line = inp.readline()
    ll = line.strip('\n').split('\t')
    for sample in ll[1:]:
      if ('Pos' not in sample) and ('Neg' not in sample) and ('.Control' not in sample):
        subprocess.run(['python3', 'entero_data_harmonize.py', sample])
        subprocess.run(['r', 'enterotyping.r'])
        inp_r = open('r_output.txt', 'r')
        lines = inp_r.readlines()
        oup.write('%s\t%s\n' % (sample, '|'.join(lines).replace('\n', '')))
        inp_r.close()
    inp.close()
    subprocess.run(['rm', '-r', folder])



