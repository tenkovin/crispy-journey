gmx editconf -f $1.pdb -o $1.gro -c -box 5.4 5.4 8.2
gmx solvate -cp $1.gro -cs tip3.gro -o $1_solv.gro -p topol.top
pymol $1_solv.gro &
echo 'anykey when use remove_water, saved retaining order'
read varname
### open pymol, use remove_water, save retaining order
python3 count.py $1.pdb TIP3 3
gedit topol.top &
echo 'anykey when used count, edited topol.top water'
read varname1
gmx editconf -f $1_solv_cut.pdb -o $1_solv_cut.gro -c -box 5.8 5.8 8.2
gmx grompp -f ions.mdp -c $1_solv_cut.gro -p topol.top -o ions.tpr
printf TIP3 | gmx genion -neutral -conc 0.15 -pname POT -nname CLA -p topol.top -o $1_solv_ions.gro -s ions.tpr
gmx make_ndx -f $1_solv_ions.gro -o index.ndx < choice.txt
csh test_run.csh
