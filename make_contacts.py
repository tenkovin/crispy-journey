import sys, math

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

def get_inputs():
    if (not len(sys.argv) == 5):
        print('\nUsage: make_contacts.py (mar.3)_itp_file (mar.3)_pdb_file EPSILON CUTOFF\n')
        sys.exit()
    else:
        atoms_file_name = sys.argv[1]
#        atoms_file_name = "Protein_A.itp" #!!!!!!!!!!!!!
        pdb_file_name = sys.argv[2]
#        pdb_file_name = "protein.pdb" #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        epsilon = float(sys.argv[3])
#        epsilon = 9.414 #!!!!!!!!!!!!!!!!!!!!
        cutoff = float(sys.argv[4])
#        cutoff = 5
        atoms_name = atoms_file_name.split('/')[-1].split('.')[0]
        pdb_name = pdb_file_name.split('/')[-1].split('.')[0]
        print('files readed: %s.itp, %s.pdb' % (atoms_name, pdb_name))
        return atoms_file_name, pdb_file_name, epsilon, cutoff

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

def get_block_indexes(array, block):
    array = atoms_array
    for i in range(len(array)):
        if ((len(array[i]) == 3) and (array[i][1] == block)):
            a = i + 1
    for i in range(a, len(array)):
        if (not array[i]):
            b = i+1; break
    return(b)

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
    return r12/10 #nanom to angstroms

def get_const(ind1, ind2):
    sigma = get_d(pdb_array, ind1, ind2)/((2)**(1/6))
    return sigma

def make_index_bb():
    index = []
    for i in range(len(atoms)):
        if atoms[i][4] == 'BB':
            index.append(atoms[i])
    return index

def make_contacts():
    contacts = []
    N = 0
    for i in range(len(index)-4):
        for j in range(i+4, len(index)):
            ind1, ind2 = int(index[i][0]), int(index[j][0])
            print('atom %s atom %s' % (ind1, ind2))
            distance = get_d(pdb_array, ind1, ind2)*10 #(nanom to ang)
            if distance < cutoff: #angstroms
                N += 1
                contact = ind1, ind2, 1, get_const(ind1, ind2), epsilon
                contacts.append(contact)
    print('(%s) contacts found, cutoff = (%s)' % (N, cutoff))
    return(contacts)

def get_output(file):
    f = open('New_pairs.txt', 'w')
    f.write('[ pairs ]')
    for i in range(len(file)):
        f.write('\n')
        f.write('{0:4d}    {1:4d}    {2:4d}    {3:15.15F}    {4:5f}'.format(*file[i]))
    f.close()
    print('New pairs saved in: ..../Working directory/New_pairs.txt')

def get_topology():
    bb = get_block_indexes(atoms_array, 'bonds')

    with open(atoms_file_name, "r") as f:
        contents = f.readlines()

    with open('New_pairs.txt', "r") as f:
        values = f.readlines()
        for i in range(len(values)):
            contents.insert(bb, values[i])
            bb += 1
        contents.insert(bb, '\n\n')
    with open(new_topology_filename, "w") as f:
        contents = "".join(contents)
        f.write(contents)
    print('Topology saved in: ..../Working directory/%s' % new_topology_filename)

#---------------------Main block-------------------------------------------------------------------------

atoms_file_name, pdb_file_name, epsilon, cutoff = get_inputs()
new_topology_filename = ("Topology_cutoff_%s.itp" % cutoff)

atoms_array = get_file_string_array(atoms_file_name)
pdb_array = get_file_string_array(pdb_file_name)

atoms = get_blocks(atoms_array, 'atoms')
index = make_index_bb()


print(index)

get_output(make_contacts())
get_topology()
