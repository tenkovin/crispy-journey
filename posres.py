import sys, math

a = []
for i in range(344):
    a.append('{0:5d}    1    {1}    {1}    {1}'.format(i+1, 'POSRES_FC'))
print(a)
with open('posres.txt', 'w') as f:
    for line in a:
        f.write(line + '\n')
