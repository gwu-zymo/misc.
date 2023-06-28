#run gut report analysis (need to build a docker file with packages installed)
#need folder sample_ID; for example: pbg0530.230511.zymo 1235364
import sys, subprocess

folder = sys.argv[1]
sample = sys.argv[2]

subprocess.run(['sudo', 'apt', 'update', '-y'])
subprocess.run(['sudo', 'apt', 'install', 'python3-pip', '-y'])
subprocess.run(['pip3', 'install', 'numpy'])
subprocess.run(['pip3', 'install', 'matplotlib'])

subprocess.run(['unzip', f"{folder}.zip"])
subprocess.run(['python3', 'parse_tax_abd_lists.py', folder, sample])
subprocess.run(['python3', 'create_abundance_figure.py', f"keystone_{sample}.txt"])
subprocess.run(['python3', 'create_abundance_figure.py', f"pathway_compiled_{sample}.txt"])
subprocess.run(['python3', 'create_abundance_figure.py', f"top_10_bac_{sample}.txt"])
subprocess.run(['mkdir', 'analysis_results'])
subprocess.run(f"mv *_{sample}.txt analysis_results", shell=True)
subprocess.run(f"mv *.png analysis_results", shell=True)





