import numpy as np
import MDAnalysis
import matplotlib.pyplot as plt
import pandas as pd

u = MDAnalysis.Universe('pull2.tpr','pull2.xtc')


def get_pos(i):
    cho = u.select_atoms('resid '+str(i))
    amb = u.select_atoms('resname AMB')
    time = []
    dist = []
    for tes in u.trajectory:
        time.append(u.trajectory.time)
        cho = u.select_atoms('resid '+str(i))
        amb = u.select_atoms('resname AMB')
        cho_cen = cho.center_of_mass()
        amb_cen = amb.center_of_mass()
        dist_ = np.linalg.norm((cho_cen - amb_cen))
        dist.append(dist_)
    return [time,dist]

np_dist = np.array(get_pos(9))
plt.plot(np_dist[0],np_dist[1])


df = pd.DataFrame(np_dist.T, columns = (['time']+['9']))

hh = np.linspace(start=3, stop=19, num = 8)

required_dist = [i for i in hh] # list of required distances
result = [[i] for i in required_dist] #
len(required_dist)
#i расстояния
k = 0
for i in required_dist:
    result_index = df.sub(i).abs().idxmin()
    value = df.loc[result_index['9'],'9']
    time = df.loc[result_index['9'],'time']
#    print(str(i) + ' : ' + str(value) + ', time = ' + str(time))
    result[k].append(time)
    result[k].append(value)
    k += 1


df1 = pd.DataFrame(result, columns = ['Req_dist', 'time, ps', 'distance'])


real_dist = df1['distance'].apply(lambda x:round(x,2)).tolist()

result[:3]

!mkdir conf

k = 0
for line in result:
    k += 1
    distance = str(line[0])
    time = str(line[1])[:-2]
    u.trajectory[int(time)]
    all = u.select_atoms('all')
    all.write('conf/conf_'+str(k)+'.gro')
# u.trajectory[49]
# all = u.select_atoms('all')
# all.write('amb6_cho_9.gro')

k = 0
for i in real_dist:
    k += 1
    conf = 'conf_'+str(k)+'.gro'
    print(conf+', '+'distance, A = '+str(i))
    with open(f'equilib_{k}.mdp', 'w') as f:
        f.write(f"""
integrator              = md
dt                      = 0.002
nsteps                  = 500000

nstcomm                 = 10
nstvout                 = 50000
nstfout                 = 50000
nstxtcout               = 250000       ; every 1 ps
nstenergy               = 50000
nstcalcenergy           = 100
nstlog                  = 1000
;
cutoff-scheme           = Verlet
nstlist                 = 20
rlist                   = 1.2
vdwtype                 = Cut-off
vdw-modifier            = Force-switch
rvdw_switch             = 1.0
rvdw                    = 1.2
coulombtype             = PME
rcoulomb                = 1.2
;
tcoupl                  = Nose-Hoover
tc_grps                 = MEMB SOLV
tau_t                   = 1.0 1.0
ref_t                   = 300 300
;
pcoupl                  = Parrinello-Rahman
pcoupltype              = semiisotropic
tau_p                   = 5.0
compressibility         = 4.5e-5  4.5e-5
ref_p                   = 1.0     1.0
refcoord_scaling        = com
;
constraints             = h-bonds
constraint_algorithm    = LINCS
continuation            = yes
;
gen_vel = no
pbc = xyz
comm_mode               = linear
comm_grps               = MEMB SOLV
; Pull code

pull                    = yes
pull-nstxout            = 100
pull-nstfout            = 100
pull_ncoords            = 1         ; only one reaction coordinate
pull_ngroups            = 2         ; two groups defining one reaction coordinate

pull_group1_name        = AMB
pull_group2_name        = ERG1
pull_coord1_type        = umbrella  ;
pull_coord1_start       = yes       ; define initial COM distance > 0
pull_coord1_rate        = 0
pull_coord1_init        = {round((i*0.1),3)}
pull_coord1_geometry    = distance  ; simple distance increase
pull_coord1_dim         = Y Y Y
pull_coord1_groups      = 1 2
pull_coord1_k           = 2      ; kJ mol^-1 nm^-2

        """)
