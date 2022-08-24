
cmd.select('Phosphor', "name P*")
ext = cmd.get_extent('Phosphor')
lower = str(ext[0][2] + 7)
upper = str(ext[1][2] - 7)

cmd.select('water_between', f'resname TIP3 and z < {upper} and z >  {lower}')
cmd.select('new_water', 'byres water_between')
cmd.remove('new_water')
