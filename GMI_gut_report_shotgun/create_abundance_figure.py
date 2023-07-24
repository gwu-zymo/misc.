#take in a sample abundance list table, such as keystone species, and generate the figures
#need the healthy sample abundance table
import matplotlib.pyplot as plt
import numpy as np
import os, sys

healthy_all = {}
inp = open('Healthy_Gut_Cohort_Species_Taxa_V1.csv', 'r')
line = inp.readline()
line = inp.readline()
while line:
  ll = line.strip('\n').split(',')
  old_name = ll[0].split(';')[-1]
  g = old_name.split(' ')[0].lstrip('s__').split('_')[0]
  s = old_name.split(' ')[1].split('_')[0]
  name = f"{g} {s}"
  if name not in healthy_all:
    healthy_all[name] = list(map(float, ll[1:]))
  else:
    healthy_all[name] = [x + y for x, y in zip(healthy_all[name], list(map(float, ll[1:])))] 
  line = inp.readline()
inp.close()

healthy_all['Christensenella sp.'] = healthy_all['Christensenella minuta']
healthy_all['Ruminococcus sp.'] = healthy_all['Ruminococcus bromii']

inp = open('Healthy_pathway.txt', 'r')
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  name = ll[0]
  if name not in healthy_all:
    healthy_all[name] = list(map(float, ll[1:]))
  line = inp.readline()
inp.close()

inp = open('healthy_ratios.txt', 'r')
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  name = ll[0]
  if name not in healthy_all:
    numbers = list(map(float, ll[1:]))
    filtered_numbers = list(filter(lambda num: num <= 10000 and num >= 0.0001, numbers))
    healthy_all[name] = filtered_numbers
  line = inp.readline()
inp.close()

inp = open(sys.argv[1], 'r')
line = inp.readline()
while line:
  ll = line.strip('\n').split('\t')
  spe = ll[0]
  abd = float(ll[1])
  if spe in healthy_all:
    abd_list = healthy_all[spe]
    abd_list.append(abd)
    numbers = np.array(abd_list)
    fig, ax = plt.subplots(figsize=(2, 12))
    violin = ax.violinplot(numbers)
    ax.plot(1, abd, 'ro')
    ax.axis('off')
    plt.savefig(f"{spe.replace(' ', '_')}_violin_plot.png", transparent=True)
  line = inp.readline()
inp.close()






  
