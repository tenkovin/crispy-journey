import pandas as pd
import sys

base_name=sys.argv[1]
prm_name=sys.argv[2]

base_name='base.prm'
pars_name='pars.prm'

!sed '/IMPROPER/,$d' $pars_name | sed '/^!/d' | sed '1,/DIHEDRALS/d' | sed 's/  / /g' | sed 's/  / /g' | sed 's/  / /g' | sed 's/  / /g' | sed 's/  / /g' > pars_cut_dih_!.txt
!cut -d "!" -f 1 $base_name | sed 's/  / /g' | sed 's/  / /g' | sed 's/  / /g' | sed 's/  / /g' | sed 's/  / /g' | sed 's/  / /g' | sed 's/  / /g' | sed 's/  / /g' > base_nospaces.txt
pars = pd.read_csv('pars_cut_dih_!.txt',sep =' ', header = None)
base = pd.read_csv('base_nospaces.txt',sep =' ', header = None)
pars = pars.dropna(axis = 1)
base = base.dropna(axis = 1)
pars = pars[[0,1,2,3]]

base_list = base.values.tolist()
pars_list = pars.values.tolist()

found_list, not_found_list = [], []
result = []
found = False
for par in pars_list:
    found = False
    for line in base_list:
        if (line[:4] == par) or (line[:4] == par[::-1]):
            print('found!')
            print(par)
            print(line)
            result.append(line)
            found_list.append(line)
            found = True
    if not found:
        result.append(par)
        not_found_list.append(par)
        print('not found..')
        print(par)


f=open('result.txt','w')
for ele in result:
    f.write('\t'.join((map(str, ele)))+'\n')

f.close()

f=open('not_found.txt','w')
for ele in not_found_list:
    f.write('\t'.join((map(str, ele)))+'\n')

f.close()

f=open('found.txt','w')
for ele in found_list:
    f.write('\t'.join((map(str, ele)))+'\n')

f.close()
