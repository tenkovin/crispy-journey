import numpy as np
import MDAnalysis
import matplotlib.pyplot as plt
import pandas as pd

u = MDAnalysis.Universe('step6.6_equilibration.tpr','step6.6_equilibration.xtc')


def get_pos(i):
    cho = u.select_atoms('resid '+str(i))
    amb = u.select_atoms('resname AMB')
    time = []
    dist = []
    for tes in u.trajectory:
        time.append(u.trajectory.time)
        cho = u.select_atoms('resid '+str(i))
        amb = u.select_atoms('resname AMB')
        dist_ = np.linalg.norm((cho.center_of_mass()- amb.center_of_mass()))
        dist.append(dist_)
    return [time,dist]


all_dist = [get_pos(1)[0]]
print(len(all_dist))
for i in range(1,15):
    all_dist.append(np.array(get_pos(i)[1]))

np_dist = np.array(all_dist)

df = pd.DataFrame(np_dist.T, columns = (['time']+[i for i in range(1,15)]))

result_index = df.sub(19).abs().idxmin()

resid = [[i] for i in range(1,15)]

for i in range(1,15):
    value = df.loc[result_index[i],i]
    time = df.loc[result_index[i],'time']
    print(str(i) + ' : ' + str(value) + ', time = ' + str(time))
    resid[i-1].append(time)
    resid[i-1].append(value)

df1 = pd.DataFrame(resid, columns = ['Number of residue', 'time, ps', 'distance'])

print(df1)

# u.trajectory[45]
# all = u.select_atoms('all')
# all.write('amb6_cho_9.gro')
