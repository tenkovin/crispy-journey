import sys, math

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
    if (not len(sys.argv) == 5):
        print('\nUsage: my.py itp_pairs(mar.2)_FILE itp_atoms(mar.3)_FILE pdb(mar.3)_FILE EPSILON\n')
        sys.exit()
    else:
        pairs_file_name = sys.argv[1]
        atoms_file_name = sys.argv[2]
        pdb_file_name = sys.argv[3]
        epsilon = sys.argv[4]

        pairs_name = pairs_file_name.split('/')[-1].split('.')[0]
        atoms_name = atoms_file_name.split('/')[-1].split('.')[0]
        pdb_name = pdb_file_name.split('/')[-1].split('.')[0]
        print('files readed:'), print(pairs_name), print(atoms_name), print(pdb_name)
        return pairs_file_name, atoms_file_name, pdb_file_name, epsilon

#takes data blocks from .itp files
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

#gets end of 'bonds' block index
def get_block_indexes(array, block):
    array = atoms_array
    for i in range(len(array)):
        if ((len(array[i]) == 3) and (array[i][1] == block)):
            a = i + 1
    print('opening bonds block line in resulting topology: (%s)' % (a))
    for i in range(a, len(array)):
        if (not array[i]):
            b = i+1; break
    print('closing bonds block line in resulting topology, pairs block will be added after that line: (%s)' % (b))
    return(b)

#gets d between atoms ind1 and ind2 in array = pdb_file
def get_d(array, ind1, ind2):

    for i in range(0, len(array)):
        if (array[i][0] == 'ATOM'): a = i; break
    for i in range(a,len(array)):
        if (array[i][0] != 'ATOM'): b = i; break
    for i in range(a,b):
        if (int(array[i][1]) == ind1):
            x1 = float(array[i][6]); y1 = float(array[i][7]); z1 = float(array[i][8]); break
    for i in range(a,b):
        if (int(array[i][1]) == ind2):
            x2 = float(array[i][6]); y2 = float(array[i][7]); z2 = float(array[i][8]); break
    r12 = math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    return r12/10 #ang to nanometers

#calculates sigma from d
def get_const(ind1, ind2):
    sigma = get_d(pdb_array, ind1, ind2)/((2)**(1/6))
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
        #new_array[i][3] = get_c6((new_array[i][0]),(new_array[i][1]))
        #new_array[i][4] = get_c12(new_array[i][0],new_array[i][1])
        new_array[i][3] = get_const((new_array[i][0]),(new_array[i][1]))
        new_array[i][4] = epsilon
    return(new_array)

#writes reindexated pairs into new_pairs.txt file
def get_output(file):
    with open('New_pairs.txt', 'w') as f:
        f.write('[ pairs ]')
        for i in range(len(file)):
            f.write('\n')
        #for j in range(len(file[i])):
            f.write('{0:4d}    {1:4d}    {2:4s}    {3:15.15F}    {4:5s}'.format(*file[i]))
    print('New pairs saved in: ..../Working directory/New_pairs.txt')

#writes final topology file with pairs added after 'bonds'
def get_topology():

    bb = get_block_indexes(atoms_array, 'bonds')

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

pairs_array = get_file_string_array(pairs_file_name)
atoms_array = get_file_string_array(atoms_file_name)
pdb_array = get_file_string_array(pdb_file_name)


#takes 2-d array of atoms in pairs_FILE and in atoms_FILE, and 2-d array of pairs in pairs_FILE
at1 = get_blocks(pairs_array, 'atoms')
at2 = get_blocks(atoms_array, 'atoms')
pr1 = get_blocks(pairs_array, 'pairs')

#mapping
_map_ = get_mapping(at1, at2)

#indexation
new_pairs_array = get_indexation(pr1, _map_)

print(new_pairs_array[3])
#creates new file new_pairs.txt, writes new pairs
get_output(new_pairs_array)

get_topology()
