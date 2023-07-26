import csv
import re
import sys
import pandas as pd

# sampleID = '5BW' 
sampleID = sys.argv[1]
folder = sys.argv[2]
# read csv file

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        # create variable to read file
        reader = csv.reader(file)
        row = list(reader)
        # print(rows)
        return row

def read_healthy_phylum_file(phylum_file_path):
    key_value_pairs = {}
    with open(phylum_file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        # row = list(reader)
        # print(row)
        row_num = 0 
        for row in reader:
            row_num += 1
            # skips the first 2 rows in the file to avoid string errors
            if row_num >= 3:
                key = row[0]
                value = float(row[2])
                key_value_pairs[key] = value
        return(key_value_pairs)

def read_sample_phylum_file(file_path):
    df = pd.read_csv(file_path, sep='\t', skiprows=1)
    
    nameArray = ["d__Bacteria;p__Bacteroidota", "d__Bacteria;p__Firmicutes", "d__Bacteria;p__Actinobacteriota", "d__Bacteria;p__Proteobacteria", "d__Bacteria;p__Verrucomicrobiota"]
    sample_key_value_pair = {}
    # print(df)
    for name in nameArray:
        sample_to_find = name 
        filtered_rows = df[df['#OTU ID'] == sample_to_find]
        sample_value = filtered_rows[sampleID].values[0]
        
        sample_key_value_pair[name] = sample_value
        
    return sample_key_value_pair

# edit css content
def edit_css_score (score_data):
    score = score_data[0]
    userScore = float(score[0])
    maxScore = 250
    
    # margin for bar shift 0.02 is 0% and 0.97 is 100%
    
    percentage = 100 * (userScore/maxScore)
    
    # converts value into a string 
    percentage = f'left: {percentage}'+'%'
    return percentage

def generate_phylum_graph(sample_phylum_data, healthy_phylum_data):
    sample = sample_phylum_data
    healthy = healthy_phylum_data 
    # name array is the order of HTML file bars, if order is changed the bars wont correlate with the right bacteria name
    nameArray = ["d__Bacteria;p__Bacteroidota", "d__Bacteria;p__Firmicutes", "d__Bacteria;p__Actinobacteriota", "d__Bacteria;p__Proteobacteria", "d__Bacteria;p__Verrucomicrobiota"]
    
    percentage_array = []
    
    import math
    
    for name in nameArray:   
        
        # multiply percentage by 0.25 for scaling relative to healthy sample(add 50 because healthy starts at 50% in css)
        sample_percentage = (((((sample[name]-healthy[name])/healthy[name])) * 100 * 0.25)+ 50)
        sample_percentage = math.floor(sample_percentage)
        percentage_array.append(sample_percentage)
        # print(sample[name])    
       
    bar_graph_css = f"#graph1{{ width: {percentage_array[0]}%}} #graph2{{ width: {percentage_array[1]}%}} #graph3{{ width: {percentage_array[2]}%}} #graph4{{ width: {percentage_array[3]}%}} #graph5{{ width: {percentage_array[4]}%}}"
    
    
    # convert data from string to float
    return(bar_graph_css)



    # file path
score_file_path = f'./{sampleID}_analysis_results/{sampleID}_HealthScore.csv'
healthy_phylum_path = f'../References/HealthyProkaryotePhylaOfInterestSummary.csv'        
sample_phylum_path = f'.{folder}/00...AllSamples.illumina.pe/Prokaryote/AbundanceTables/2.Phylum/phylum.tsv'


# read the file and store in variable
score_data = read_csv_file(score_file_path)

healthy_phylum_data = read_healthy_phylum_file(healthy_phylum_path)
sample_phylum_data = read_sample_phylum_file(sample_phylum_path)

# run function to edit file that was read to generate css edits
sample_score = edit_css_score(score_data)
phylum_graph = generate_phylum_graph(sample_phylum_data, healthy_phylum_data)

# css content to be modified
score_css_content = '/* arrow position */'
phylum_graph_css_content = '/* populate all phylum graphs */'
# open css template and modify with new styling
    # file path
with open ('style_template.css', 'r') as file:
    css_content = file.read()

modified_css_content = css_content.replace(score_css_content, sample_score)
modified_css_content = modified_css_content.replace(phylum_graph_css_content, phylum_graph)
with open ('style.css', 'w') as file:
    file.write(modified_css_content)  
    print("CSS styling modified and saves to style.css")      
    
    


