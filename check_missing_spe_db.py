import os, sys

kyle = {}
inp = open('kyle.txt', 'r')
line = inp.readline()
while line:
  kyle[line.strip('\n').split('.')[0]] = ''
  line = inp.readline()
  line = inp.readline()
inp.close()

all = {}
for file in os.listdir('./run/'):
  key = file.split('.')[0]
  all[key] = []
  if key in kyle:
    all[key].append('done')
  else:
    all[key].append('not')
  all[key].append('1')


for file in os.listdir('./run2/'):
  key = file.split('.')[0]
  if not key in all:
    all[key] = []
    if key in kyle:
      all[key].append('done')
    else:
      all[key].append('not')
  else:
    all[key][-1] = all[key][-1] + '2'
  
oup = open('summary.txt', 'w')
for key in all:
  oup.write('%s\t%s\n' % (key, '\t'.join(all[key])))
oup.close()
