import itertools as it
with open('lig.prm', 'r') as file:
    lig = file.readlines()
with open('new.prm', 'r') as file:
    new = file.readlines()



filtered = list(filter(lambda s: ' !' in s, lig))
print(len(filtered))
splitted_ligs = list(map(lambda s:  s[:(s.index('!')+1)].split(), filtered))
print(splitted_ligs)

lig_bonds = list(filter(lambda l: len(l) == 5, splitted_ligs))
lig_angles = list(filter(lambda l: (len(l) == 6 or (len(l) == 8 and l[3].replace('.', '').isdigit())), splitted_ligs))
lig_dihedrals = list(filter(lambda l: l[3].replace('.', '').isdigit() == False , splitted_ligs))

splitted_pars = list(map(lambda s: s.split(), list(filter(lambda l: '  !' in l[-5::], new[:new.index('IMPROPER\n'):]))))

new_bonds = list(filter(lambda l: len(l) == 5, splitted_pars))
new_angles = list(filter(lambda l: len(l) == 6, splitted_pars))
new_dihedrals = list(filter(lambda l: len(l) == 8, splitted_pars))

bonds = []
for line_new in new_bonds:
   for line_lig in lig_bonds:
       if tuple(line_new[:2]) in list(it.permutations(line_lig[:2],2)):
           print('for '+str(line_new)+ ' bond parameters taken:')
           print(line_lig)
           print('-------------')
           bonds.append(line_lig)

angles = []
for line_new in new_angles:
   for line_lig in lig_angles:
       if line_new[:3] == line_lig[:3] or line_new[:3] ==  line_lig[2::-1]:
           print('for '+str(line_new)+ ' angle parameters taken:')
           print(line_lig)
           print('-------------')
           angles.append(line_lig)

dihedrals = []
for line_new in new_dihedrals:
   for line_lig in lig_dihedrals:
       if line_new[:4] == line_lig[:4] or line_new[:4] ==  line_lig[3::-1]:
           print('for '+str(line_new)+ ' dihedral parameters taken:')
           print(line_lig)
           print('-------------')
           dihedrals.append(line_lig)
           break
print(len(dihedrals))

result =[['BONDS']]+ bonds + [['ANGLES']] + angles + [['DIHEDRALS']] + dihedrals
with open('output.txt', 'w') as file:
    for line in result:
        file.write('\n'+'\t'.join(line))
