
gmx editconf -f $1.pdb -o $1.gro -c -box 5.546 5.546 8.2
python3 count.py $1.gro ERG 73 POPC 134 > counts.txt
cat topol_empty.top counts.txt > topol.top
gmx solvate -cp $1.gro -cs tip3.gro -o $1_solv.gro -p topol.top

python3 remove_water_2.py $1_solv.gro $1_solv_cut.pdb

python3 count.py $1_solv_cut.pdb ERG 73 POPC 134 TIP3 3 > counts.txt
cat topol_empty.top counts.txt > topol.top

gmx editconf -f $1_solv_cut.pdb -o $1_solv_cut.gro -c -box 5.546 5.546 8.2
gmx grompp -f ions.mdp -c $1_solv_cut.gro -p topol.top -o ions.tpr -maxwarn -1
printf TIP3 | gmx genion -neutral -conc 0.15 -pname POT -nname CLA -p topol.top -o $1_solv_ions.gro -s ions.tpr
gmx make_ndx -f $1_solv_ions.gro -o index.ndx < choice.txt
csh README $1
