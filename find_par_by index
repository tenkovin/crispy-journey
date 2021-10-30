import sys

prm_name = sys.argv[1]
psf_name = sys.argv[2]
with open(prm_name, 'r') as file:
    prm_lines = file.readlines()
with open(psf_name, 'r') as file:
    psf_lines = file.readlines()

#--------------------------------TYPE (psf)---------------------------------------

psf_split = list(map(lambda l: l.split(), psf_lines))
psf = list(filter(lambda l: len(l) == 11, psf_split))

#index = list(map(lambda s: str(int(s)+1) ,['49', '22', '23', '18']))
index = list(map(lambda s: str(int(s)+1) ,sys.argv[3:]))
type = []
for i in index:
    atom = list(filter(lambda s: s[0] == i, psf))[0]
    type.append(atom[5])


#-----------------------------prm--------------------------------------------------

filtered = list(filter(lambda s: ' !' in s, prm_lines))

prm_split = list(map(lambda s:  s.split(), filtered)) #[:(s.index('!')+1)]


prm_bonds = list(filter(lambda l: len(l[:l.index('!')+1]) == 5, prm_split))
prm_angles = list(filter(lambda l: (len(l[:l.index('!')+1]) == 6 or (len(l[:l.index('!')+1]) == 8 and l[3].replace('.', '').isdigit())), prm_split))
prm_dihedrals = list(filter(lambda l: l[3].replace('.', '').isdigit() == False , prm_split))

#def get_penalty(matrix, types)
#    filtered = list(filter(lambda l: 'PENALTY=' in l, matrix))


for line_prm in prm_dihedrals:
       if type == line_prm[:4] or type ==  line_prm[3::-1]:
           print('for '+str(type)+ ' dihedral parameters taken:')
           print(line_prm)
           print('-------------')
           break
