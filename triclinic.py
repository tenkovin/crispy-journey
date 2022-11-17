#!/usr/bin/env python
# coding: utf-8

# In[101]:


get_ipython().system('gmx editconf -f inter5.pdb  -o inter5.gro -bt triclinic -box 4.95 4.95 5.8 -angles 90 90 60 -rotate 0  0 70 -c')


# In[102]:


get_ipython().system('python2 count.py inter5.gro LIG 138 ERG 73 POP 134 TIP3 3 CLA 2 POT 2')


# In[103]:


with open('inter5.gro', 'r') as file:
    lines = file.readlines()

start = 1480
prev_res = 14
length = 134
for res in range(1,17):
    start_line = start + (res-1)*length
    end_line = start_line + length
    res_number = prev_res + res
    for line in range(start_line-1,end_line-1):
        lines[line] = lines[line].replace(' 4POP ',str(f'{res_number}POPC'))

with open('inter5_ren.gro', 'w') as file:
    for line in lines:
        file.writelines(line)


# In[10]:


get_ipython().system('gmx solvate -cp inter5_ren.gro -cs tip3.gro -o solv.gro')


# In[11]:


get_ipython().system('python2 count.py solv.gro TIP3 3')


# In[14]:



from pymol import cmd
import sys
cmd.set('retain_order',1)
cmd.load('solv.gro')
cmd.select('Phosphor', "name N*")
ext = cmd.get_extent('Phosphor')
lower = str(ext[0][2] + 7)
upper = str(ext[1][2] - 7)

cmd.select('water_between', f'resname TIP3 and z < {upper} and z >  {lower}')
cmd.select('new_water', 'byres water_between')
cmd.remove('new_water')
cmd.save('solv_cut.pdb')

get_ipython().system('gmx editconf -f solv_cut.pdb  -o solv_cut.gro -bt triclinic -box 4.95000   4.28683   5.20000 -angles 90 90 60 -rotate 0  0 0')
# !gmx editconf -f water.pdb  -o water.gro
# !sed '1,2d' water.gro > testt.gro
# !sed '$d' testt.gro > testtt.gro
# !sed '$d' testtt.gro > testttt.gro


# In[96]:


get_ipython().system('cp solv_cut.gro count.py /home/shiba1/dogge38i/home/dogge38-i/Desktop/Valera/channel/someplace')

