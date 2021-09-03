import sys, math
import numpy as np
import MDAnalysis
from MDAnalysis.analysis import distances

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

#Gives proper usage of the script, takes file names and epsilon which will be used
def get_inputs():
    # if (not len(sys.argv) == 5):
    #     print('\nUsage: my.py itp_pairs(mar.2)_FILE itp_atoms(mar.3)_FILE pdb(mar.3)_FILE EPSILON\n')
    #     sys.exit()
    # else:
        # pairs_file_name = sys.argv[1]
        # atoms_file_name = sys.argv[2]
        # pdb_file_name = sys.argv[3]
        # epsilon = sys.argv[4]
        pairs_file_name = 'Protein_A_2.itp'
        atoms_file_name = 'molecule_0.itp'
        pdb_file_name = 'protein3.pdb'
        epsilon = '9.414'
        return pairs_file_name, atoms_file_name, pdb_file_name, epsilon

#gets block indexes
def get_block_indexes(array, block):
    for i in range(len(array)):
        if ((len(array[i]) == 3) and (array[i][1] == block)):
            a = i + 1
    for i in range(a, len(array)):
        if (not array[i]):
            b = i; break
    print('(%s) index (%s)' % (a, b))
    return a,b

#takes data blocks from .itp files
def get_blocks(array, block):
    bl = []
    a,b = get_block_indexes(array, block)
    for i in range(a,b):
        bl.append(array[i])
    return bl

#gets d between atoms ind1 and ind2 in array = pdb_file
def get_d(ind1, ind2): #gets index list starting from 1, gives d for index list starting from 0!
    ind1 = ind1 - 1
    ind2 = ind2 - 1
    atom1 = u.select_atoms('index '+str(ind1))
    atom2 = u.select_atoms('index '+str(ind2))
    r12 = distances.dist(atom1,atom2, offset = 0)[2]
    return r12[0]

    print(get_d(3,11)/(((2)**(1/6))*10))
    print(get_const(3,11))
#calculates sigma from d
def get_const(ind1, ind2):
    sigma = get_d(ind1, ind2)/(((2)**(1/6))*10) #nanom
    return sigma

#checks for equality the number of residue, name of residue, and type of atom (BB, SC1, SC2, etc) in two files
#and comes out with 2xi array of mapping
def get_mapping(m1, m2):
    map = []
    for i in range(0,len(m1)):
        map.append([i+1])
        for j in range(0,len(m2)):
            if ((m1[i][2] == m2[j][2]) and (m1[i][3] == m2[j][3]) and (m1[i][4] == m2[j][4])):
                map[i].append(j+1)
    return(map)

#changes number of atoms interacting and rewrites constants to sigma(i,j) and epsilon according to mapping
def get_indexation(array, map):
    for i in range(0,len(array)):
        new_array = array
        new_array[i][0] = map[int(array[i][0])-1][1]
        new_array[i][1] = map[int(array[i][1])-1][1]
        new_array[i][3] = get_const((new_array[i][0]),(new_array[i][1]))
        new_array[i][4] = epsilon
    return(new_array)

#writes reindexated pairs into new_pairs.txt file
def get_output(file):
    with open('New_pairs.txt', 'w') as f:
        f.write('[ pairs ]')
        for i in range(len(file)):
            f.write('\n')
            f.write('{0:4d}    {1:4d}    {2:4s}    {3:15.15F}    {4:5s}'.format(*file[i]))
    print('New pairs saved in: ..../Working directory/New_pairs.txt')

#writes final topology file with pairs added after 'bonds'
def get_topology():

    bb = get_block_indexes(atoms_array, 'bonds')[1] + 1

    with open(sys.argv[2], "r") as f:
        contents = f.readlines()

    with open('New_pairs.txt', "r") as f:
        values = f.readlines()
        for i in range(len(values)):
            contents.insert(bb, values[i])
            bb += 1
        contents.insert(bb, '\n\n')
    with open("New_topology.itp", "w") as f:
        contents = "".join(contents)
        f.write(contents)
    print('Topology saved in: ..../Working directory/New_topology.itp')
#---------------------Main block-------------------------------------------------------------------------

pairs_file_name, atoms_file_name, pdb_file_name, epsilon = get_inputs()

u = MDAnalysis.Universe(pdb_file_name)
print(u)

pairs_array = get_file_string_array(pairs_file_name)
atoms_array = get_file_string_array(atoms_file_name)
pdb_array = get_file_string_array(pdb_file_name)

#takes 2-d array of atoms in pairs_FILE and in atoms_FILE, and 2-d array of pairs in pairs_FILE
at1 = get_blocks(pairs_array, 'atoms')
at2 = get_blocks(atoms_array, 'atoms')
pr1 = get_blocks(pairs_array, 'pairs')

#mapping
_map_ = get_mapping(at1, at2)
array = np.array(_map_)
print(_map_)

#indexation
new_pairs_array = get_indexation(pr1, _map_)

print(new_pairs_array[1])
#creates new file new_pairs.txt, writes new pairs
get_output(new_pairs_array)

get_topology()
