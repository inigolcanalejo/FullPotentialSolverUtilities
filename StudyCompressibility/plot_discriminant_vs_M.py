import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

directory = '/media/inigo/10740FB2740F9A1C/Results/12_phd/method/discriminant'
def WritePlotToFile(file_name, x, y):
    with open(file_name, 'w') as file_write:
        for i in range(len(x)):
            file_write.write('{0:15f} {1:15f}\n'.format(x[i], y[i]))

# Input
free_stream_speed_of_sound = 340.0
heat_capacity_ratio = 1.4

hcr = heat_capacity_ratio
ai2 = free_stream_speed_of_sound * free_stream_speed_of_sound
ai4 = ai2 * ai2
print(' free_stream_speed_of_sound = ', free_stream_speed_of_sound)

free_stream_mach_number = 0.8

free_stream_velocity = free_stream_mach_number * free_stream_speed_of_sound

print('\n free_sream_mach_number     = ', round(free_stream_mach_number,1))
print(' free_stream_velocity       = ', round(free_stream_velocity,1))

# Computing squares and shortening names
Mi2 = free_stream_mach_number**2
vi2 = free_stream_velocity**2

vacuum_speed2 = vi2 * (1 + 2 / ((hcr-1)*Mi2))
vacuum_speed = math.sqrt(vacuum_speed2)
print('vacuum_speed = ', vacuum_speed)

velocity = np.arange(0., 750.0, 1.0)

v2 = velocity**2

square_brackets_term = 1.0 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)
local_speed_of_sound2 = ai2 * square_brackets_term
local_speed_of_sound4 = local_speed_of_sound2 * local_speed_of_sound2

local_mach2 = Mi2 * v2 / (vi2 * square_brackets_term)
local_mach = np.sqrt(local_mach2)

discriminant = 4 * local_speed_of_sound4 * (local_mach2 - 1) / ai4

filename = directory + '/discriminant_vs_M.dat'
WritePlotToFile(filename, local_mach, discriminant)

plt.plot(local_mach, discriminant, label='discriminant')

plt.legend(loc="lower left")
plt.xlabel('discriminant dimensionless')
plt.ylabel('local mach')
plt.grid()
plt.show()