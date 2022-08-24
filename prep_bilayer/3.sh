gmx editconf -f $1_solv_cut.pdb -o $1_solv_cut.gro -c -box 5.8 5.8 8.2
gmx grompp -f ions.mdp -c $1_solv_cut.gro -p topol.top -o ions.tpr
printf TIP3 | gmx genion -neutral -conc 0.15 -pname POT -nname CLA -p topol.top -o $1_solv_ions.gro -s ions.tpr
gmx make_ndx -f $1_solv_ions.gro -o index.ndx < choice.txt
csh README_2

