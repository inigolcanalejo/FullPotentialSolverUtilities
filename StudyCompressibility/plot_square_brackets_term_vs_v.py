import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

directory = '/media/inigo/10740FB2740F9A1C/Results/12_phd/method/limit_velocity/square_brackets_term'
def WritePlotToFile(file_name, x, y):
    with open(file_name, 'w') as file_write:
        for i in range(len(x)):
            file_write.write('{0:15f} {1:15f}\n'.format(x[i], y[i]))

# Input
free_stream_speed_of_sound = 340.0
heat_capacity_ratio = 1.4

hcr = heat_capacity_ratio
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

velocity = np.arange(0., 805.0, 1.0)

v2 = velocity**2

square_brackets_term = 1.0 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

local_mach2 = Mi2 * v2 / (vi2 * square_brackets_term)

numerator = 1.0 + (hcr - 1) / 2.0 * Mi2
denominator = 1.0 + (hcr - 1) / 2.0 * local_mach2

square_brackets_term_mach = numerator / denominator

density_non_dim = pow(square_brackets_term_mach, 1/(hcr-1))

filename = directory + '/density_non_dim_vs_v.dat'
WritePlotToFile(filename, velocity, density_non_dim)

plt.plot(velocity, square_brackets_term, label='square brackets term')
plt.plot(velocity, density_non_dim, label='density')

plt.legend(loc="lower left")
plt.xlabel('velocity')
plt.ylabel('square brackets term')
plt.grid()
plt.show()