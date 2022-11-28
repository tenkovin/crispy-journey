#!/usr/bin/env python
# coding: utf-8

# In[40]:


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import numpy as np
import pandas as pd
import subprocess as sp


# In[41]:


from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


# In[42]:


#Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)


# In[43]:


sheet = client.open_by_key('1VFhAoyh-bbwuFEQMDkq15Pm4Qlsfvc7uvBc-aHdt0KA')
worksheet = sheet.get_worksheet(0)
python_sheet = worksheet.get_all_records()
pp = pprint.PrettyPrinter()
# pp.pprint(python_sheet)
df = pd.DataFrame(python_sheet)

df.replace('', np.nan, inplace=True)
df.dropna(subset=['id'], inplace=True)


# In[44]:


load = [['свободен'] for i in range(0,6)]
testtt=pd.DataFrame(load, columns =['process'])
testtt


# In[55]:


machines = {
'dogge38':'dogge38@dogge38',
'dogge38+':'dogge38-i@dogge38i',
'dogge37':'dogge37@dogge',
'shiba1':'shiba1@shiba1',
'dogge':'dogge@dogge1',
'lab1':'lab1@lab221',
}

get_ipython().system("parallel-ssh -i -h ~/hosts -- ps aux | grep 'gmx mdrun' > load.log")
get_ipython().system("ps aux | grep 'gmx mdrun' | grep -v 'grep' >> load.log")

with open(f'load.log', 'r') as file:
    lines = file.readlines()

lines1 = []
lines2 = []

for line in lines:
    line1 = line.split("gmx")[0]
    lines1.append(line1.split())

    line2 = line.split("gmx")[1]
    
    pid = (line1.split()[1])
    machine = machines[line1.split()[0]]
    if line1.split()[0] == 'shiba1':
         dir = str(sp.check_output(f"pwdx {pid} | awk '{{print $2}}'", shell=True))[2:-3]
    else:
        dir = str(sp.check_output(f"ssh {machine} 'pwdx {pid}' | awk '{{print $2}}'", shell=True))[2:-3]
    lines2.append([line2[:-1],dir])

df1 = pd.DataFrame(lines1)

df2 = pd.DataFrame(lines2, columns=['10','11'])

df3 = pd.concat([df1,df2], axis = 1)

df3 = df3.drop([1,2,3,4,5,6,7,9], axis=1)

df3.columns = ['A', 'B', 'C','D']
df3


# In[51]:


def check_load(id: str,data):
    if id in data['A'].to_numpy():
        proc = data.loc[df3['A'] == id, 'C'].item()
    else:
        proc = 'свободен'
    
    return(proc)

def check_load_directory(id: str,data):
    if id in data['A'].to_numpy():
        proc = data.loc[df3['A'] == id, 'D'].item()
    else:
        proc = '-'
    
    return(proc)


# In[52]:


df_res = df[['id']]
df_res['process']=df_res['id'].apply(lambda x: check_load(x,df3))
df_res['directory']=df_res['id'].apply(lambda x: check_load_directory(x,df3))
df_res


# In[53]:


load = np.array(df_res[['process']]).tolist()
load1 = [[dt_string]]
load2 = np.array(df_res[['directory']]).tolist()

if not df[['process']].equals(df_res[['process']]):
    print("updating...", dt_string)	

    worksheet.batch_update([{
        'range': 'H2:H7',
        'values': load,
    },
    {
        'range': 'I2:I7',
        'values': load2,
    },
    {
        'range': 'B10',
        'values': load1,
    }
    ])

