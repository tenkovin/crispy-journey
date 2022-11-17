#!/usr/bin/env python
# coding: utf-8

# In[43]:


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import numpy as np
import pandas as pd


# In[44]:


from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


# In[45]:


#Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)


# In[46]:


sheet = client.open_by_key('...') #enter key of your spreadsheet
worksheet = sheet.get_worksheet(0)
python_sheet = worksheet.get_all_records()
pp = pprint.PrettyPrinter()
# pp.pprint(python_sheet)
df = pd.DataFrame(python_sheet)

df.replace('', np.nan, inplace=True)
df.dropna(subset=['id'], inplace=True)


# In[48]:


get_ipython().system("parallel-ssh -i -h ~/hosts -- ps aux | grep 'gmx mdrun' > load.log")

with open(f'load.log', 'r') as file:
    lines = file.readlines()

lines1 = []
lines2 = []
for line in lines:
    line1 = line.split("gmx")[0]
    lines1.append(line1.split())
    line2 = line.split("gmx")[1]
    lines2.append(line2[:-2])

df1 = pd.DataFrame(lines1)

df2 = pd.DataFrame(lines2, columns=['10'])

df3 = pd.concat([df1,df2], axis = 1)

df3 = df3.drop([1,2,3,4,5,6,7,9], axis=1)

df3.columns = ['A', 'B', 'C']


# In[49]:


def check_load(id: str,data):
    if id in data['A'].to_numpy():
        proc = data.loc[df3['A'] == id, 'C'].to_numpy()[0]
    else:
        proc = 'свободен'
    
    return(proc)


# In[50]:

df_res = df[['id']]

df_res.loc[:,'process']=df.loc[:,'id'].apply(lambda x: check_load(x,df3))


# In[51]:


load = np.array(df_res[['process']]).tolist()
load1 = [[dt_string]]

if not df[['process']].equals(df_res[['process']]):
    print("updating...", dt_string)	

    worksheet.batch_update([{
        'range': 'H2:H7',
        'values': load,
    },{
        'range': 'B10',
        'values': load1,
    }
    ])


# %%
