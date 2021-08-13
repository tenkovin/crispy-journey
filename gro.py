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

def process(array):
    b = len(array)
    print(b)
    for line in array:
        if (line[0] == 'ATOM'):
            line.insert(4, 'A')
    print(array[10])
    return array


def get_output(file):
    with open('New_renum.txt', 'w') as f:
        for i in range(0, len(file)):
            f.write('{0:4s}{1:>7s}  {2:3s}{3:>4s}{4:>2s}{5:>4s}{6:>12s}{7:>8s}{8:>8s}{9:>6s}{10:>6s}{11:>12s}'.format(*file[i]))
            f.write('\n')
    print('New pairs saved in: ..../Working directory/New.txt')



#content = get_file_string_array('6z5l_AA.pdb')
#print(proc[10][0])
#proc = process(content)
#print(len(content))
#print(len(proc))
#get_output(proc)

content = get_file_string_array('New.txt')

count = 0
for line in content:
    line[1] = str(count+1)
    content[count] = line
    count += 1

get_output(content)
