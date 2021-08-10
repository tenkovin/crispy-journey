import numpy as np
import MDAnalysis
import matplotlib.pyplot as plt
import math

u = MDAnalysis.Universe('longrun.tpr', 'longrun.xtc')
tpr_resid_from_one=False
print(u)
#------FUNCTIONS----------

# read file data into a 2-d array
def get_file_string_array(file_name):
    try:
        file = open(file_name, "r")
    except IOError:
        print('Error: file (%s) not found!\n' % (file_name))
        sys.exit()
    lines = file.readlines()
    file.close()
    array = []
    for line in lines:
        array.append(line.split())
    return array

# Get blocks of data by their name
def get_blocks(array, block):
    bl = []
    for i in range(len(array)):
        if ((len(array[i]) == 3) and (array[i][1] == block)):
            a = i + 1; break
    print('(%s) opening index: (%s)' % (block, a))
    for i in range(a, len(array)):
        if (not array[i]):
            b = i
            break
    print('(%s) closing index: (%s)' % (block, b))
    for i in range(a,b):
        bl.append(array[i])
    return bl

#Get distance between two atoms
def distance(ind1, ind2): #gets index list starting from 1, gives d for index list starting from 0!
    ind1 = ind1 - 1
    ind2 = ind2 - 1
    atom1 = u.select_atoms('index '+str(ind1))
    atom2 = u.select_atoms('index '+str(ind2))
    delta = atom2.positions[0]-atom1.positions[0]
    r12 = math.sqrt(delta[0]**2+delta[1]**2+delta[2]**2)
    return r12

#Count contacts in one frame
def count_contacts():
    n = 0
    for i in range(len(contacts)):
        ind1 = int(contacts[i][0]); ind2 = int(contacts[i][1])
        if ((distance(ind1, ind2)/10 < 2*(float(contacts[i][3]))) and (check_inchain(ind1, ind2) == True)):
            n += 1
    return n

#calculates sigma from d
def get_const(ind1, ind2):
    sigma = distance(ind1, ind2)/((2)**(1/6))
    #C6 = 4*9.414*sigma**6; C12 = 4*9.414*sigma**12
    #return C6, C12
    return sigma


def check_inchain(ind1, ind2):
    inchain = False
    pair = ind1, ind2
    if (pair in helix12) or (pair in helix23) or (pair in helix13):
        inchain = True
    else:
        pair = ind2, ind1
        if (pair in helix12) or (pair in helix23) or (pair in helix13):
            inchain = True
    return inchain


#------------------MAIN----------------------------

pairs_array = get_file_string_array('Protein_A.itp')
contacts = get_blocks(pairs_array, 'pairs')

helix1 = list(range(370, 415, 1))
helix2 = list(range(415, 475, 1))
helix3 = list(range(475, 534, 1))

helix12, helix23, helix13 = []
for index in contacts:
    if (index[0] in helix1 and index[1] in helix2) or (index[0] in helix2 and index[1] in helix1):
        helix12.append([index[0], index[1]])
    elif (index[0] in helix1 and index[1] in helix3) or (index[0] in helix3 and index[1] in helix1):
        helix13.append([index[0], index[1]])
    elif (index[0] in helix2 and index[1] in helix3) or (index[0] in helix3 and index[1] in helix2):
        helix23.append([index[0], index[1]])



time = []
contacts_trj = []

for tes in u.trajectory:
    contacts_trj.append(count_contacts())
    time.append(u.trajectory.time/1000)


fig, ax = plt.subplots()

ax.plot(time, contacts_trj, '--', color='black', linewidth=2)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.tick_params(width=3, labelsize=13)
fig.savefig("plot.png", format='png', dpi=600)
print('plot.png saved to working directory')
