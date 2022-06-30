import numpy as np
import MDAnalysis
import matplotlib.pyplot as plt
from itertools import combinations
from matplotlib import ticker, cm
from iteration_utilities import deepflatten
import pandas as pd
import seaborn as sns
from scipy.signal import savgol_filter
#-----------------------------------------------------FILES
!ls ../*tpr > names.txt
with open('names.txt') as f:
    content = f.read().splitlines()
    f.close()

tmin=1000

names = list(map(lambda x: x[3:-4], content))
#types_ = [['C2','C18'],['C27','C5']]
#types_ = [['C3','C23'],['O9','C5']]
types_ = [['C3','C23'],['C27','C5']]
types = []
for name in names:
    if 'amb6' in name:
        types.append(types_[1])
    else:
        types.append(types_[0])

zipped = list(zip(names, types))
flat = [[item[0],item[1][0],item[1][1]] for item in zipped ]

#-----------------------------------------------------CALC


def get_pos(name,nonpolar,polar):
    u = MDAnalysis.Universe('../'+name+'.tpr', '../pbc_'+name+'.trr')
    print('../'+name+'.tpr', '../pbc_'+name+'.trr')
    print(u)
    atoms_vec = u.select_atoms('resname AMB and name '+nonpolar, 'resname AMB and name '+polar)
    print('resname AMB and name '+nonpolar,'resname AMB and name '+polar)
    print(atoms_vec)
    time = []
    vec_pos = []
    for tes in u.trajectory[tmin:]:
        time.append(u.trajectory.time)
        vec_pos.append(atoms_vec.positions[:2])
    return [name,[vec_pos,time]]

def get_vector(positions):
    vec1 = []
    for vec in positions:
        vec1.append([vec[0][0] - vec[1][0], vec[0][1] - vec[1][1], vec[0][2] - vec[1][2]])
    return(vec1)

def unit_vector(vector):
    new_vector = []
    for vec in vector:
        new_vector.append(list(vec / np.linalg.norm(vec)))
    return np.array(new_vector)

def get_angle(vectors):
    angle = []
    for vector in vectors:
        angle.append(round(np.arccos(np.dot(vector, normale))*57.2958))
    return angle

def probability(angles):
    prob = []
    angle = []
    ang_sum = len(angles)
    for i in range(1, 180):
        angle.append(i)
        prob.append(angles.count(i)/ang_sum)
    return angle, prob

normale = np.array([0,0,1])

all_vecs = []
for item in flat:
    name, nonpolar, polar = item
    all_vecs.append(get_pos(name, nonpolar, polar))

vecs_dict=dict(all_vecs)

for name in vecs_dict:
    print(name)
    vec_pos, time = vecs_dict[name]
    vec = np.array(get_vector(vec_pos))
    norm_vec = unit_vector(vec)
    angles = get_angle(norm_vec)
    angle, prob = probability(angles)
    print(len(time))
    with open(name+'_angle1000.dat', 'w') as f:
        for i in range(len(angle)):
            f.write(str(angle[i]) + ' ' + str(prob[i]) +'\n')
        f.close()
        with open(name+'_vec2.dat', 'w') as f:
            for i in range(len(time)):
                f.write(str(angles[i]) + ' ' + str(time[i]) +'\n')
        f.close()

df_z_cho_amb = pd.read_csv('cho_amb_vec2.dat', sep = ' ', names = ['Угол, ДПФХ/Хол/АмБ', 'время'])
df_z_cho_amb6 = pd.read_csv('cho_amb6_vec2.dat', sep = ' ', names = ['Угол, ДПФХ/Хол/АмБ-амф', 'время'])
df_z_erg_amb = pd.read_csv('erg_amb_vec2.dat', sep = ' ', names = ['Угол, ДПФХ/Эрг/АмБ', 'время'])
df_z_erg_amb6 = pd.read_csv('erg_amb6_vec2.dat', sep = ' ', names = ['Угол, ДПФХ/Эрг/АмБ-амф', 'время'])
df_z_dmpc_amb = pd.read_csv('dmpc_amb_vec2.dat', sep = ' ', names = ['Угол, ДПФХ/АмБ', 'время'])
df_z_dmpc_amb6 = pd.read_csv('dmpc_amb6_vec2.dat', sep = ' ', names = ['Угол, ДПФХ/АмБ-амф', 'время'])


merged_df_z = pd.concat([df_z_cho_amb,df_z_cho_amb6,df_z_erg_amb,df_z_erg_amb6,df_z_dmpc_amb,df_z_dmpc_amb6],axis = 1, join='outer')
df_z = merged_df_z.T.groupby(level=0).first().T
#sns.relplot(x='Угол, градусы',y = 'value', hue="variable", kind="line", data=pd.melt(df, ['Угол, градусы']))


df2_z = df_z.apply(lambda x: savgol_filter(x,31,3), axis = 0)
df2_z.plot('время','Угол, ДПФХ/Хол/АмБ')
df2_z.plot('время','Угол, ДПФХ/Хол/АмБ-амф')
df2_z.plot('время','Угол, ДПФХ/Эрг/АмБ')
df2_z.plot('время','Угол, ДПФХ/Эрг/АмБ-амф')
df2_z.plot('время','Угол, ДПФХ/АмБ')
df2_z.plot('время','Угол, ДПФХ/АмБ-амф')


df_cho_amb = pd.read_csv('cho_amb_angle1000.dat', sep = ' ', names = ['Угол, градусы', 'ДПФХ/Холестерин/AmB'])
df_cho_amb6 = pd.read_csv('cho_amb6_angle1000.dat', sep = ' ', names = ['Угол, градусы', 'ДПФХ/Холестерин/AmB-амфамид'])
df_erg_amb = pd.read_csv('erg_amb_angle1000.dat', sep = ' ', names = ['Угол, градусы', 'ДПФХ/Эргостерин/AmB'])
df_erg_amb6 = pd.read_csv('erg_amb6_angle1000.dat', sep = ' ', names = ['Угол, градусы', 'ДПФХ/Эргостерин/AmB-амфамид'])
df_dmpc_amb = pd.read_csv('dmpc_amb_angle1000.dat', sep = ' ', names = ['Угол, градусы', 'ДПФХ/AmB'])
df_dmpc_amb6 = pd.read_csv('dmpc_amb6_angle1000.dat', sep = ' ', names = ['Угол, градусы', 'ДПФХ/AmB-амфамид'])

merged_df = pd.concat([df_cho_amb,df_cho_amb6,df_erg_amb,df_erg_amb6,df_dmpc_amb,df_dmpc_amb6],axis = 1, join='outer')
df = merged_df.T.groupby(level=0).first().T
#sns.relplot(x='Угол, градусы',y = 'value', hue="variable", kind="line", data=pd.melt(df, ['Угол, градусы']))


df2 = df.apply(lambda x: savgol_filter(x,9,3), axis = 0)

plot_cho.set_ylabel('Вероятность')
plot_erg.set_ylabel('Вероятность')
plot_dmpc.set_ylabel('Вероятность')
plot_cho = df2.plot('Угол, градусы', ['ДПФХ/Холестерин/AmB','ДПФХ/Холестерин/AmB-амфамид'] )
plot_cho.set_ylabel('Вероятность')
plt.savefig('1.png', dpi = 300)
plot_erg = df2.plot('Угол, градусы', ['ДПФХ/Эргостерин/AmB','ДПФХ/Эргостерин/AmB-амфамид'] )
plot_erg.set_ylabel('Вероятность')
plt.savefig('2.png', dpi = 300)
plot_dmpc = df2.plot('Угол, градусы', ['ДПФХ/AmB','ДПФХ/AmB-амфамид'])
plot_dmpc.set_ylabel('Вероятность')
plt.savefig('3.png', dpi = 300)

plot_cho.set_ylabel('Вероятность')
plot_erg.set_ylabel('Вероятность')
plot_dmpc.set_ylabel('Вероятность')
