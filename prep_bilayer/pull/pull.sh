cp step6*gro start.gro
gmx make_ndx -f start.gro -n index.ndx < choice.txt
gmx grompp -f pull-1.mdp -c start.gro -n index.ndx -p topol.top -o pull-1.tpr -maxwarn -1
gmx mdrun -v -deffnm pull-1
printf 0 | gmx trjconv -f pull-1.xtc  -s pull-1.tpr -o pull-1.gro -dump 9999999
gmx grompp -f pull1.mdp -c pull-1.gro -n index.ndx -p topol.top -o pull1.tpr -maxwarn -1
gmx mdrun -v -deffnm pull1
