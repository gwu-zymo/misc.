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
  
  if 'bscess' not in line:
    count = False
  
  if count == True:
    ll = line.strip('\n').split(',')
    ID = ll[65]
    for i in range(0, len(ll)):
      if header[i].startswith('k_'):
        if ll[i] != '':
          if not header[i] in spe_ct:
            spe_ct[header[i]] = 1
          else:
            spe_ct[header[i]] = spe_ct[header[i]] + 1
  line = inp.readline()
inp.close()
            
oup = open('bunny_face_abscess.txt', 'w')
for spe in spe_ct:
  oup.write('%s\t%i\n' % (spe, spe_ct[spe]))
oup.close()
