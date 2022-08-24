import re
import sys

with open(sys.argv[1], 'rt') as f:
    contents = f.read()

MOL = [re.compile(sys.argv[n]) for n in range(2, len(sys.argv), 2)]
ATOMS = [sys.argv[n] for n in range(3, len(sys.argv), 2)]
molec = [sys.argv[n] for n in range(2, len(sys.argv), 2)]


n_molec = []
for element in MOL:
    n_molec.append(len(element.findall(contents)))

for i, (n_m, n_a) in enumerate(zip(n_molec, ATOMS)):
    n_molec[i] = int(n_m)/int(n_a)

for i in range(len(n_molec)):
    print('number of ' +molec[i]+ " = {}".format(n_molec[i]))
