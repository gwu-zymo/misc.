import os, boto3

s3 = boto3.client("s3", region_name="us-east-1")

response = s3.list_objects_v2(
    Bucket='midog'
    )

data = response['Contents']

while 'Contents' in response:
    response = s3.list_objects_v2(
        Bucket='midog',
        StartAfter=response['Contents'][-1]['Key']
        )
    data.extend(response['Contents'])

zipfile = {}
for key in data:
    file = key['Key']
    if file.endswith('.zip') and 'rawdata' in file:
        zipfile[file] = ''
        
project = {}
oup = open('rawdata_midog.txt', 'w')
for file in zipfile:
    fs = file.split('/')
    key = fs[1]
    date = fs[-1].split('.')[2]
    if key not in project:
        project[key] = [date]
    else:
        project[key].append(date)
        
    s3.download_file('midog', file, fs[-1])
    os.system('unzip %s' % fs[-1])
    os.system('rm *.zip')
    f_path = '/'.join(fs[:-1])
    s_path = '%s/miniseq_$s/%s' % (f_path, date, gz)
    for gz in os.listdir('./'):
        s3.upload_file(gz, 'zymo-filesystem', s_path)
        os.system('rm ')
    oup.write('%s\t%s\n' % (key, ))
oup.close()
    
s3.download_file('midog', 'Projects/md0392/rawdata/md0392.rawdata.220727.zip', 'md0392.rawdata.220727.zip')
s3.uploadload_file('md0392_1c_R2.fastq.gz', 'zymo-filesystem', 'tmp/gwu_test/md0392_1c_R2.fastq.gz')
   
