import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
# import imageio
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

# Input
free_stream_speed_of_sound = 340.0
heat_capacity_ratio = 1.4
free_stream_density = 1.0

hcr = heat_capacity_ratio
ai2 = free_stream_speed_of_sound * free_stream_speed_of_sound
print(' free_stream_speed_of_sound = ', free_stream_speed_of_sound)

free_stream_mach_number = 0.8

free_stream_velocity = free_stream_mach_number * free_stream_speed_of_sound
print('\n free_sream_mach_number     = ', round(free_stream_mach_number,1))
print(' free_stream_velocity       = ', round(free_stream_velocity,1))

# Computing squares and shortening names
Mi2 = free_stream_mach_number**2
vi2 = free_stream_velocity**2

density_list = []
term_2_list = []
local_mach_list = []
jacobian_list = []
filenames = []

directory = '/media/inigo/10740FB2740F9A1C/Results/12_phd/method/terms'

for velocity in range(0,400):
    v2 = velocity**2

    square_brackets_term = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

    density = free_stream_density * pow(square_brackets_term, 1/(hcr-1))

    term_2 = pow(square_brackets_term, (2-hcr)/(hcr-1)) * v2 / ai2

    local_mach2 = Mi2 * v2 / (vi2 * square_brackets_term)
    local_mach = np.sqrt(local_mach2)

    density_list.append(density)
    term_2_list.append(term_2)
    local_mach_list.append(local_mach)
    jacobian_list.append(density - term_2)

    plt.plot(local_mach_list, density_list, label='term 1 $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(local_mach_list, term_2_list,  label='term 2 $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(local_mach_list, jacobian_list, label='Difference $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.grid()
    axes = plt.gca()
    axes.set_xlim([0.0, 1.2])
    axes.set_ylim([-0.5,1.5])

    filename = directory + '/terms_' + "{:03d}".format(velocity) + '.png'
    print('filename = ', filename)
    filenames.append(filename)

    #save
    plt.savefig(filename)
    plt.close()

# # build gif
# with imageio.get_writer('mygif.gif', mode='I') as writer:
#     for filename in filenames:
#         image = imageio.imread(filename)
#         writer.append_data(image)

# # remove files
# for filename in set(filenames):
#     os.remove(filename)

# plt.legend(loc="lower left")
# plt.xlabel('local mach')
# plt.ylabel('density')
# plt.grid()
# plt.show()