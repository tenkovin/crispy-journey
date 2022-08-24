import numpy as np
import pandas as pd
list = np.round(np.linspace(0,54.5,5),2)



#list = np.round(np.linspace(0,4,5),2)
#with open('restraints.inp', 'w') as f:

list_of_coords = []
for i in list:
    for j in list:
        list_of_coords.append([np.array([i,j])])


for item in list_of_coords:
    dot2 = item[0]+np.array([13.62,13.62])
    if (68.12 not in dot2):
        item.append(dot2)


df = pd.DataFrame(list_of_coords, columns = ['first', 'second'])
array = df.dropna().to_numpy()
array = array.tolist()
array_=list(map(lambda x: x.tolist(),array))

with open('restraints.inp', 'w') as f:
    i = 0
    for item in array:
        i=i+1
        dot1 = item[0]
        dot2 = item[1]
        print(i, dot1, dot2)

        f.write(f"""
structure erg1.pdb #lower, {i}-th square
  number 1 #
  inside box {str(dot1[0]).replace('.',',')}. {str(dot1[1]).replace('.',',')}. 0. {str(dot2[0]).replace('.',',')}. {str(dot2[1]).replace('.',',')}. 26.
  atoms 2 #polar
    below plane 0. 0. 1. 9. #(24-15)
  end atoms
  atoms 60 #non polar
    over plane 0. 0. 1. 23. #(26-2)
  end atoms
end structure

structure erg1.pdb #higher, {i}-th square
  number 1 #
  inside box {str(dot1[0]).replace('.',',')}. {str(dot1[1]).replace('.',',')}. 26. {str(dot2[0]).replace('.',',')}. {str(dot2[1]).replace('.',',')}. 52.
  atoms 60 #non polar
    below plane 0. 0. 1. 30. #(24-15)
  end atoms
  atoms 2 #polar
    over plane 0. 0. 1. 44. #(26-2)
  end atoms
end structure
"""

          )
