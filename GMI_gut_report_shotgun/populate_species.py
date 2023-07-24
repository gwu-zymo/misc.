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
        table_body += f'<tr><td>{row[0]}</td><td>{dot_html}</td><td>{row[1]}%</td></tr>'
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
    for index, row in enumerate(species):
        if index >= 10:
            break 
        table_body += f'<tr><td>{row[0]}</td><td>{(row[1]):.4f}</td></tr>'
        
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
    pathogen_img = '<img src="./images/graphs/page7/pathogen.svg" alt="pathogen" width="20px">'
    keystone_img = '<img src="./images/graphs/page7/keystone.svg" alt="keystone" width="20px">'
    
    table_body = ''
    for index, data in enumerate(bacteria):
        if index >= 12:
            break
        species_name = data[0]
        if species_name in pathogen_name:
            table_body += f'<tr><td>{data[0]}</td><td>{pathogen_img}</td><td>{float(data[1]):.4f}</td></tr>'
        elif species_name in keystone_name:
            table_body += f'<tr><td>{data[0]}</td><td>{keystone_img}</td><td>{float(data[1]):.4f}</td></tr>'
        else:
            table_body += f'<tr><td></td><td></td><td></td></tr>'
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
    for index, row in enumerate(species):
        if index >= 12:
            break
        table_body += f'<tr><td>{row[0]}</td><td>{(row[1]):.4f}</td></tr>'
    for _ in range(index + 1, 12):
        table_body += '<tr><td></td><td></td></tr>'
    return table_body    
        
            
def generate_patient_info(tsv_data):
    data = tsv_data[0]
    info_body= f'<p>Patient: {data["Patient Name"]}<br> Sex: {data["Sex"]}<br> DOB: {data["DOB"]}<br> Sample ID: {data["SampleID"]}</p>'
    return info_body


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
        short_chain_fatty_acid = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['short chain fatty acids'])]))
        butyrate = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['butyrate'])]))
        acetate = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['acetate'])]))
        propionate = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['propionate'])]))
        prancreatic_elastase = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['short chain fatty acids'])]))
        calprotectin = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['short chain fatty acids'])]))
        vitamin_synthesis = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['vitamin synthesis'])]))
        folate = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['folate'])]))
        riboflavin = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['riboflavin'])]))
        b12 = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['B12'])]))
        bile_acid = "{:.5f}".format(statistics.median([float(num) for num in (key_value_pair['bile acid'])]))
        
        metabolite_array = [short_chain_fatty_acid, butyrate, acetate, propionate, prancreatic_elastase, calprotectin, vitamin_synthesis, folate, riboflavin, b12, bile_acid]
        return metabolite_array



####################################
#~~~~DEFINE AND READ FILE PATHS~~~~#
####################################

# Specify the path to TSV file
    # file path
    pathogen_tsv_file_path = sys.argv[1]
    
# pathogen_tsv_file_path = f'./{sampleID}_analysis_results/pathogen_5BW.txt'
# keystone_txt_file_path = f'./{sampleID}_analysis_results/keystone_1235364.txt'
# bacteria_txt_file_path = f'./{sampleID}_analysis_results/top_10_bac_1235364.txt'
# fungal_txt_file_path = f'./{sampleID}_analysis_results/top_10_fun_1235364.txt'

pathogen_tsv_file_path = f'./{sampleID}_analysis_results/pathogen_{sampleID}.txt'
keystone_txt_file_path = f'./{sampleID}_analysis_results/keystone_{sampleID}.txt'
bacteria_txt_file_path = f'./{sampleID}_analysis_results/top_10_bac_{sampleID}.txt'
fungal_txt_file_path = f'./{sampleID}_analysis_results/top_10_fun_{sampleID}.txt'


patient_tsv_file = './patient_input_files/patient_info.txt'
enterotype_file_path = './analysis_results/sample_r_output.txt'

range_file_path = './patient_input_files/Healthy_pathway.txt'

# Read the TSV file and set as variable to pass into the table function
pathogen_tsv_data = read_txt_file(pathogen_tsv_file_path)
keystone_tsv_data = read_txt_file(keystone_txt_file_path)
bacteria_tsv_data = read_txt_file(bacteria_txt_file_path)
fungal_tsv_data = read_txt_file(fungal_txt_file_path)

patient_tsv_data = read_patient_tsv_file(patient_tsv_file)
enterotype_out_data = read_out_file(enterotype_file_path)


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

metabolite = read_generate_metabolic_values(range_file_path)

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


#####~MODIFIED CONTENT IN HTML~#####
 
# Replace the table body content in the HTML with the generated table
modified_html_content = html_content.replace(pathogen_html_content, pathogen_table)
modified_html_content = modified_html_content.replace(keystone_html_content, keystone_table)
modified_html_content = modified_html_content.replace(bacteria_html_content, bacteria_table)
modified_html_content = modified_html_content.replace(fungal_html_content, fungal_table)

modified_html_content = modified_html_content.replace(patient_info_html_content, patient_info)
modified_html_content = modified_html_content.replace(enterotype_number_html_content, enterotype_number)
modified_html_content = modified_html_content.replace(enterotype_description_html_content, enterotype_description)

# Modify Content for images generated from analysis results 
modified_html_content = modified_html_content.replace("[sampleID]", sampleID_string)

# Modify content for metabolites
modified_html_content = modified_html_content.replace('~Short Chain Fatty Acid~', metabolite[0])
modified_html_content = modified_html_content.replace('~Butyrate~', metabolite[1])
modified_html_content = modified_html_content.replace('~Acetate~', metabolite[2])
modified_html_content = modified_html_content.replace('~Propionate~', metabolite[3])
modified_html_content = modified_html_content.replace('~Pancreatic Elastase~', metabolite[4])
modified_html_content = modified_html_content.replace('~Calprotectin~', metabolite[5])
modified_html_content = modified_html_content.replace('~Vitamin Synthesis~', metabolite[6])
modified_html_content = modified_html_content.replace('~Folate~', metabolite[7])
modified_html_content = modified_html_content.replace('~Riboflavin~', metabolite[8])
modified_html_content = modified_html_content.replace('~B12~', metabolite[9])
modified_html_content = modified_html_content.replace('~Bile Acid~', metabolite[10])


# replace metabolic html content


# Write the modified HTML back to the file
    # file path
output_file_path = 'output.html'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(modified_html_content)



print('HTML table modified and saved to', output_file_path)
