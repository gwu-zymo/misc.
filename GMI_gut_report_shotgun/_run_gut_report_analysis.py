#run gut report analysis (need to build a docker file with packages installed)
#need folder sample_ID; for example: pbg0530.230511.zymo 1235364
import sys, subprocess

folder = sys.argv[1]
sample = sys.argv[2]

subprocess.run(['sudo', 'apt', 'update', '-y'])
subprocess.run(['sudo', 'apt', 'install', 'r-cran-littler', '-y'])
subprocess.run(['sudo', 'apt', 'install', 'python3-pip', '-y'])
subprocess.run(['pip3', 'install', 'numpy'])
subprocess.run(['pip3', 'install', 'matplotlib'])
subprocess.run(['pip3', 'install', 'pandas'])
subprocess.run(f"sudo apt install libcurl4-openssl-dev libssl-dev libxml2-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev -y", shell=True)

subprocess.run(f"sudo Rscript get_donut_plot.r {folder} {sample}", shell=True)
subprocess.run(['unzip', f"{folder}.zip"])
subprocess.run(['python3', 'parse_tax_abd_lists.py', folder, sample])
subprocess.run(['python3', 'create_abundance_figure.py', f"keystone_{sample}.txt"])
subprocess.run(['python3', 'create_abundance_figure.py', f"pathway_compiled_{sample}.txt"])
subprocess.run(['python3', 'create_abundance_figure.py', f"top_10_bac_{sample}.txt"])
subprocess.run(['python3', 'user_total_commensal.py', folder, sample])
subprocess.run(['python3', 'user_gut_score.py', folder, sample])
subprocess.run(['python3', 'alpha_div_graph.py', folder, sample])
subprocess.run(f"mkdir {sample}_analysis_results", shell=True)
subprocess.run(f"mv *{sample}*.* {sample}_analysis_results", shell=True)
subprocess.run(f"mv *.png {sample}_analysis_results", shell=True)
subprocess.run(['python3', 'entero_data_harmonize.py', folder, sample])
subprocess.run(['r', 'enterotype_classifier.r'])
subprocess.run(f"mv sample_* {sample}_analysis_results", shell=True)

subprocess.run(f"python3 rotate_figures.py {sample}", shell=True)
subprocess.run(f"python3 populate_species.py {sample}", shell=True)
subprocess.run(f"python3 edit_css.py {sample} {folder}", shell=True)
#subprocess.run(f"rm -r {folder} cluster", shell=True)
#subprocess.run(f"rm *.zip *.py *.r", shell=True)
subprocess.run(f"mv output.html {sample}_output.html", shell=True)
#subprocess.run(f"zip {sample}_results.zip ../../shotgun_wrapper/* -r", shell=True)
#subprocess.run(f"mv *.zip ../../", shell=True)
subprocess.run(f"mkdir {sample}_results", shell=True)
subprocess.run(f"mv {sample}



