import os, sys

key_words = ['oral', 'Oral', 'face', 'Face', 'mouth', 'Mouth', 'dental', 'Dental']

spe_ct = {}

inp = open('bunny_selected_samples.csv', 'r')
line = inp.readline()
header = line.strip().split(',')
line = inp.readline()
while line:
  count = False
  for key in key_words:
    if key in line:
      count = True
      break
  
  if count == True:
    ll = line.strip('\n').split(',')

