#run gut report analysis
#need folder sample_ID; for example: pbg0530.230511.zymo 1235364
import sys, subprocess

subprocess.run(['sudo', 'apt', 'update', '-y'])
subprocess.run(['sudo', 'apt', 'install', 'python3-pip', '-y'])
subprocess.run(['pip3', 'install', 'numpy'])
subprocess.run(['pip3', 'install', 'matplotlib'])


subprocess.run(['unzip', ])

result = subprocess.run(['command', 'arg1', 'arg2'])

