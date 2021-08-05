gmx editconf -f protein.pdb -d 1.0 -o protein.gro -bt cubic

gmx grompp -f minimization.mdp -p topol.top -c protein.gro -o minim-vac.tpr -maxwarn 1
gmx mdrun -v -deffnm minim-vac

gmx solvate -cp minim-vac.gro -cs water.gro -radius 0.21 -o solvated.gro -p topol.top

gmx grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr -maxwarn 1
yes "13" | gmx genion -s ions.tpr -o ion.gro -p topol.top -pname NA -nname TCL -neutral

gmx grompp -f minimization.mdp -p topol.top -c ion.gro -o minim.tpr -maxwarn 1
gmx mdrun -v -deffnm minim

gmx grompp -f equilibration.mdp -c minim.gro -p topol.top -o eq.tpr -maxwarn 1
gmx mdrun -v -deffnm eq

gmx grompp -f longrun.mdp -c eq.gro -p topol.top -o longrun.tpr -maxwarn 1
gmx mdrun -v -deffnm longrun

gmx trjconv -f longrun.xtc -o long-pbc.xtc -pbc mol -s longrun.tpr
yes "0" | gmx trjconv -f longrun.xtc -o long-pbc.xtc -pbc mol -s longrun.tpr


#vmd solvated.gro

#gmx solvate -cp minimization-vaccum.gro -cs water.gro -radius 0.21 -o solvated.gro 
