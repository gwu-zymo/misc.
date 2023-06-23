#take the healthy species abundance and generate healthy pathway ranges
import os, sys

pathway_all = {}
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

