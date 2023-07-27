import sys
import csv

# sampleID = 123

sampleID= sys.argv[1]
# projectID = sys.argv[1]
# rundate = sys.argv[2]

sampleID_string = str(sampleID)
#####################################
#~~~~READ CSV, TXT AND OUT FILES~~~~#
#####################################

# read the TSV file and return its contents as a list of rows
def read_tsv_file(file_path):
    # returns array of key value pairs with a list of rows
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        rows = list(reader)
    return rows

# returns data as an array
# example: [['Akkermansia muciniphila', '0.0163564579808'], ['Bacteroides thetaiotaomicron', '0.0046374631823'], ['Bifidobacterium longum', '0.00131603684903'], ['Christensenella sp.', '0'], ['Faecalibacterium prausnitzii', '0.20762048004'], ['Ruminococcus sp.', '0.00946293162875'], ['Bacteroides fragilis', '0'], ['Bacteroides stercoris', '0.0'], ['Eubacterium sp.', '0']]
def read_txt_file (file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        rows = list(reader)
        return rows

# read patient TSV file with tabs instead of commas
def read_patient_tsv_file (tsv_file):
    with open(tsv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        row = list(reader)
        return(row)
    
# read OUT file, taking the last value for enterotype  
def read_out_file (out_file_path):
    
    with open(out_file_path, 'r', encoding='utf-8') as file:
        # reads the file and separate content in an array
        content = file.read()
        newContent = content.split(',')
        # removes '\n' or whitespace from the enterotype number
        enterotype = newContent[-1].strip()
        # returns enterotype number as '1', '2' or '3'
        return enterotype

####################################
#~~~~GENERATE TABLES OF SPECIES~~~~#
####################################

def generate_pathogen_table(data):
    table_body = ''
    index = 0
    for index, row in enumerate(data):
        if index >= 10:
            break
        percentage = float(row[1])
        # dot_class = 'green' if percentage == 1 else('yellow' if percentage == 2 else 'red')
        if percentage == 1:
            dot_class = 'green'
        elif (1.1 <= percentage <= 1.4):
            dot_class = 'yellow'
        elif percentage > 1.5:
            dot_class = 'red'
        else:
            dot_class = ''
        dot_html = f'<span class="dot {dot_class}"></span>'
        table_body += f'<tr><td>{row[0]}</td><td>{dot_html}</td><td>{row[1]}</td></tr>'
    #Add extra rows for empty tsvdata
    for _ in range(index + 1, 10):
        table_body += '<tr><td></td><td></td><td></td></tr>'
    return table_body

def generate_keystone_table(tsv_data):
    # take species abundance and converts it to a flaot and sorts it in descending order
    species = []
    for row in tsv_data:
        name = row[0]
        number = float(row[1])
        species.append([name, number])
    species.sort(key = lambda x: x[1], reverse=True)

    table_body = ''
    index = 0
    for index, row in enumerate(species):
        if index >= 10:
            break 
        if row[1] < 0.01:
            table_body += f'<tr><td>{row[0]}</td><td> < 0.01 </td></tr>'
        else:
            table_body += f'<tr><td>{row[0]}</td><td>{(row[1]):.2f}</td></tr>'
        
    for _ in range(index + 1, 10):
        table_body += '<tr><td></td><td></td></tr>'
    return table_body

def generate_bacterial_table(bacteria_tsv_data, pathogen_tsv_data, keystone_tsv_data):
    # take list of tsv data and iterate over the rows to create table content
    
    # take species abundance and converts it to a flaot and sorts it in descending order
   
    # dictionaries of datasets
    bacteria = bacteria_tsv_data
    pathogen = pathogen_tsv_data
    keystone = keystone_tsv_data
    
    # check for species name in dataset
    pathogen_name = {item[0] for item in pathogen}
    keystone_name = {item[0] for item in keystone}
    
    # image reference for HTML
    # file path
    pathogen_img = '<img src="../References/pathogen.png" alt="pathogen" width="20px">'
    keystone_img = '<img src="../References/keystone2.png" alt="keystone" width="20px">'
    
    table_body = ''
    index = 0 
    for index, data in enumerate(bacteria):
        if index >= 12:
            break
        species_name = data[0]
        abundance = float("{:.2f}".format(float(data[1])))
        
        if abundance < 0.01:
            if species_name in pathogen_name:
                table_body += f'<tr><td>{data[0]}</td><td>{pathogen_img}</td><td> < 0.01 </td></tr>'
            elif species_name in keystone_name:
                table_body += f'<tr><td>{data[0]}</td><td>{keystone_img}</td><td> < 0.01 </td></tr>'
            else:
                table_body += f'<tr><td>{data[0]}</td><td></td><td> < 0.01 </td></tr>'
        else:
            if species_name in pathogen_name:
                table_body += f'<tr><td>{data[0]}</td><td>{pathogen_img}</td><td>{abundance}</td></tr>'
            elif species_name in keystone_name:
                table_body += f'<tr><td>{data[0]}</td><td>{keystone_img}</td><td>{abundance}</td></tr>'
            else:
                table_body += f'<tr><td>{data[0]}</td><td></td><td>{abundance}</td></tr>'
    
    for _ in range(index + 1, 12):
        table_body += '<tr><td></td><td></td><td></td></tr>'
    return table_body

def generate_fungal_table(tsv_data):
    species = []
    for row in tsv_data:
        name = row[0]
        number = float(row[1])
        species.append([name, number])
    species.sort(key = lambda x: x[1], reverse=True)
    
    table_body = ''
    index = 0
    for index, row in enumerate(species):
        if index >= 12:
            break
        if row[1] < 0.01:
            table_body += f'<tr><td>{row[0]}</td><td> < 0.01 </td></tr>'
        else:
            table_body += f'<tr><td>{row[0]}</td><td>{(row[1]):.2f}</td></tr>'
    for _ in range(index + 1, 12):
        table_body += '<tr><td></td><td></td></tr>'
    return table_body    
        
######################################
#~~~~GENERATE PATIENT INFO RATIOS~~~~#
######################################

def generate_patient_info(tsv_data):
    patient_data_dict = tsv_data
    
    patient_data = []
    
    for data in patient_data_dict:
        if data["SampleID"] == sampleID:
            patient_data.append(data)
            break
        else:
            print('Id not found')

    patient = patient_data[0]
    info_body= f'<p>Patient: {patient["Patient Name"]}<br> Sex: {patient["Sex"]}<br> DOB: {patient["DOB"]}<br> Sample ID: {patient["SampleID"]}</p>'
    
    if patient == []:
        print('No patient ID found')
    else:
        print("Patient ID successfully found")
        return info_body

def generate_metabolic_sample_ratio(ratio_data): 
    key_value_pair = {}
    
    for row in ratio_data:
        key = row[0]
        value = "{:.2f}".format(float(row[1]))
        key_value_pair[key] = float(value)
        
    firmicutes_ratio = f'<div class="ratio1"><p>{key_value_pair["Firmicutes_Bacteroidota"]}</p> </div>'
    proteobacteria_ratio = f'<div class="ratio2"><p>{key_value_pair["Proteobacteria_Actinobacteriota"]}</p> </div>'
    sample_ratio = firmicutes_ratio + proteobacteria_ratio
    
    return sample_ratio

####################################
#~~~~GENERATE ENTEROTYPE NUMBER~~~~#
####################################

def generate_enterotype_number(out_file_data):
    # create and return a string for HTML input from enterotype number
    body_info = ''
    if out_file_data == '1':
        body_info = f'<h3>Your Enterotype: 1</h3>'
    elif out_file_data == '2':
        body_info = f'<h3>Your Enterotype: 2</h3>'
    elif out_file_data == '3':
        body_info = f'<h3>Your Enterotype: 3</h3>'
    else:
        body_info = f'<h3>Your Enterotype: Not Present</h3>'
    # print(body_info)
    return body_info


def generate_enterotype_description(out_file_data):
    body_info = ''
    if out_file_data == '1':
        body_info = f'<p>Enterotype 1 is the most frequent one and is enriched in Ruminococcus. It is also enriched in membrane transporters, mostly of sugars, suggesting the efficient binding of mucin and its subsequent hydrolysis as well as uptake of the resulting simple sugars by these genera. The enriched genera suggest that enterotypes employ different routes to generate energy from fermentable substrates.</p>'
    elif out_file_data == '2':
        body_info = f'<p>Enterotype 2 is the most frequent one and is enriched in Ruminococcus. It is also enriched in membrane transporters, mostly of sugars, suggesting the efficient binding of mucin and its subsequent hydrolysis as well as uptake of the resulting simple sugars by these genera. The enriched genera suggest that enterotypes employ different routes to generate energy from fermentable substrates.</p>'
    elif out_file_data == '3':
        body_info = f'<p>Enterotype 3 is the most frequent one and is enriched in Ruminococcus. It is also enriched in membrane transporters, mostly of sugars, suggesting the efficient binding of mucin and its subsequent hydrolysis as well as uptake of the resulting simple sugars by these genera. The enriched genera suggest that enterotypes employ different routes to generate energy from fermentable substrates.</p>'
    else:
        body_info = f'<p>Sorry, your enterotype is nonexistent.</p>'
    # print(body_info)
    return body_info

####################################
#~~~~GENERATE METABOLITE VALUES~~~~#
####################################

def read_generate_metabolic_values(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        rows = list(reader)
        # print(rows[0])
        key_value_pair = {}
        for data in rows:
            key = (data[0])
            value = data[1:]
            key_value_pair[key] = value
            # print(key_value_pair)
        
        import statistics
        
        # convert string values from metabolites into floats from key value pairs
        # takes the median of all the float values
        # truncates the median value after 3 decimals (:.3f)
        short_chain_fatty_acid ="{:.2f}".format(statistics.median([float(num) for num in (key_value_pair['short chain fatty acids'])]))
        butyrate = "{:.2f}".format(statistics.median([float(num) for num in (key_value_pair['butyrate'])]))
        acetate = "{:.2f}".format(statistics.median([float(num) for num in (key_value_pair['acetate'])]))
        propionate = "{:.2f}".format(statistics.median([float(num) for num in (key_value_pair['propionate'])]))
        inflammation = "{:.2f}".format(statistics.median([float(num) for num in (key_value_pair['inflammation'])]))
        vitamin_synthesis = "{:.2f}".format(statistics.median([float(num) for num in (key_value_pair['vitamin synthesis'])]))
        folate = "{:.2f}".format(statistics.median([float(num) for num in (key_value_pair['folate'])]))
        riboflavin = "{:.2f}".format(statistics.median([float(num) for num in (key_value_pair['riboflavin'])]))
        b12 = "{:.2f}".format(statistics.median([float(num) for num in (key_value_pair['B12'])]))
        bile_acid = "{:.2f}".format(statistics.median([float(num) for num in (key_value_pair['bile acid'])]))
        
        metabolite_array = [short_chain_fatty_acid, butyrate, acetate, propionate, inflammation, vitamin_synthesis, folate, riboflavin, b12, bile_acid]
        metabolite_array_float = []
        for metabolite in metabolite_array:
            metabolite_float = float(metabolite)
            metabolite_array_float.append(metabolite_float)
        
        metabolite_value_check = []
        for metabolite in metabolite_array_float:
            if metabolite < 0.01:
                metabolite_value_check.append("< 0.01")
            else:
                metabolite_value_check.append(metabolite)
        
        return metabolite_value_check


####################################
#~~~~DEFINE AND READ FILE PATHS~~~~#
####################################

# Specify the path to TSV file
    # file path
pathogen_txt_file_path = f'./{sampleID}_analysis_results/pathogen_{sampleID}.txt'
keystone_txt_file_path = f'./{sampleID}_analysis_results/keystone_{sampleID}.txt'
bacteria_txt_file_path = f'./{sampleID}_analysis_results/top_10_bac_{sampleID}.txt'
fungal_txt_file_path = f'./{sampleID}_analysis_results/top_10_fun_{sampleID}.txt'


patient_txt_file = '../patient_info.txt'
enterotype_file_path = f'./{sampleID}_analysis_results/sample_r_output.txt'
metabolite_healthy_range_file_path = '../References/Healthy_pathway.txt'

metabolic_sample_ratio_file_path = f'./{sampleID}_analysis_results/{sampleID}_ratios.txt'

# Read the TSV file and set as variable to pass into the table function
pathogen_tsv_data = read_txt_file(pathogen_txt_file_path)
keystone_tsv_data = read_txt_file(keystone_txt_file_path)
bacteria_tsv_data = read_txt_file(bacteria_txt_file_path)
fungal_tsv_data = read_txt_file(fungal_txt_file_path)

patient_tsv_data = read_patient_tsv_file(patient_txt_file)
enterotype_out_data = read_out_file(enterotype_file_path)

sample_ratio_data = read_txt_file(metabolic_sample_ratio_file_path)

#############################################################
#~~~~GENERATE GRAPHS FUNCTION CALLS DEFINED AS VARIABLES~~~~#
#############################################################

# Generate the HTML table from tsv data 
pathogen_table = generate_pathogen_table(pathogen_tsv_data)
keystone_table = generate_keystone_table(keystone_tsv_data)
bacteria_table = generate_bacterial_table(bacteria_tsv_data, pathogen_tsv_data, keystone_tsv_data)
fungal_table = generate_fungal_table(fungal_tsv_data)

patient_info = generate_patient_info(patient_tsv_data)
enterotype_number = generate_enterotype_number(enterotype_out_data)
enterotype_description = generate_enterotype_description(enterotype_out_data)

metabolite = read_generate_metabolic_values(metabolite_healthy_range_file_path)

sample_ratio = generate_metabolic_sample_ratio(sample_ratio_data)

# Read the HTML file
    # file path
html_file_path = 'Report_Template.html'
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()


# content to be replaced, characters have to be exact as the html file parsed
pathogen_html_content = '<!-- Generated pathogen table -->'
keystone_html_content = '<!-- Generated keystone table -->'
bacteria_html_content = '<!-- Generated bacteria table -->'
fungal_html_content = '<!-- Generated fungal table -->'

patient_info_html_content = '<!-- Patient Info -->'
enterotype_number_html_content = '<!-- Generated enterotype number -->'
enterotype_description_html_content = '<!-- Generated enterotype description -->'

sample_ratio_html_content = '<!-- Generate Sample Ratio -->'
#####~MODIFIED CONTENT IN HTML~#####
 
# Replace the table body content in the HTML with the generated table
modified_html_content = html_content.replace(pathogen_html_content, pathogen_table)
modified_html_content = modified_html_content.replace(keystone_html_content, keystone_table)
modified_html_content = modified_html_content.replace(bacteria_html_content, bacteria_table)
modified_html_content = modified_html_content.replace(fungal_html_content, fungal_table)

modified_html_content = modified_html_content.replace(patient_info_html_content, patient_info)
modified_html_content = modified_html_content.replace(enterotype_number_html_content, enterotype_number)
modified_html_content = modified_html_content.replace(enterotype_description_html_content, enterotype_description)

# Add the sample ratio 
modified_html_content = modified_html_content.replace(sample_ratio_html_content, sample_ratio)

# Modify Content for images generated from analysis results 
modified_html_content = modified_html_content.replace("[sampleID]", sampleID_string)

# Modify content for metabolites
modified_html_content = modified_html_content.replace('~Short Chain Fatty Acid~', metabolite[0])
modified_html_content = modified_html_content.replace('~Butyrate~', metabolite[1])
modified_html_content = modified_html_content.replace('~Acetate~', metabolite[2])
modified_html_content = modified_html_content.replace('~Propionate~', metabolite[3])
modified_html_content = modified_html_content.replace('~Inflammation~', metabolite[4])
modified_html_content = modified_html_content.replace('~Vitamin Synthesis~', metabolite[5])
modified_html_content = modified_html_content.replace('~Folate~', metabolite[6])
modified_html_content = modified_html_content.replace('~Riboflavin~', metabolite[7])
modified_html_content = modified_html_content.replace('~B12~', metabolite[8])
modified_html_content = modified_html_content.replace('~Bile Acid~', metabolite[9])


# replace metabolic html content


# Write the modified HTML back to the file
    # file path
output_file_path = 'output.html'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(modified_html_content)



print('HTML table modified and saved to', output_file_path)
