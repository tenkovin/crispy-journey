import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI

import sys, time, os
import pymol

pymol.finish_launching()



file = sys.argv[1]
outfile = sys.argv[2]
##
# Read User Input
spath = os.path.abspath(file)
sname = spath.split('/')[-1].split('.')[0]

# Load Structures

pymol.cmd.load(spath, sname)
pymol.cmd.disable("all")
pymol.cmd.enable(sname)




pymol.cmd.set ( 'retain_order', value='1')


pymol.cmd.select('Phosphor', "name P*")
ext = pymol.cmd.get_extent('Phosphor')
lower = str(ext[0][2] + 7)
upper = str(ext[1][2] - 7)

pymol.cmd.select('water_between', f'resname TIP3 and z < {upper} and z >  {lower}')
pymol.cmd.select('new_water', 'byres water_between')
pymol.cmd.remove('new_water')

pymol.cmd.save(outfile)

# Get out!
pymol.cmd.quit()
