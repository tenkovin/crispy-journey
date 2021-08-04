gmx editconf -f protein.pdb -d 1.0 -o protein.gro -bt cubic

gmx grompp -f minimization.mdp -p topol.top -c protein.gro -o minim-vac.tpr 
gmx mdrun -v -deffnm minim-vac

gmx solvate -cp minimization-vaccum.gro -cs water.gro -radius 0.21 -o solvated.gro 

gmx grompp -f minimization.mdp -p topol.top -c solvated.gro -o minim-solv.tpr 
gmx mdrun -v -deffnm minim-solv

gmx grompp -f equilibration.mdp -c minim-solv.gro -p topol.top -o eq.tpr -r minim-solv.gro #maxwarn 1
gmx mdrun -v -deffnm eq

#gmx grompp -f equilibration.mdp -c minim-solv.gro -p topol.top -o eq.tpr -r minim-solv.gro #maxwarn 1
#gmx mdrun -v -deffnm eq

gmx grompp -f longrun.mdp -c eq.gro -p topol.top -o longrun.tpr -r eq.gro
gmx mdrun -v -deffnm longrun

gmx trjconv -f longrun.xtc -o long-pbc.xtc -pbc mol -s longrun.tpr 
vmd solvated.gro


