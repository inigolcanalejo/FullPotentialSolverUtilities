import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

# Input
free_stream_speed_of_sound = 340.0
heat_capacity_ratio = 1.4
free_stream_mach_number = 0.84

hcr = heat_capacity_ratio
ai2 = free_stream_speed_of_sound * free_stream_speed_of_sound
print(' free_stream_speed_of_sound = ', free_stream_speed_of_sound)

free_stream_velocity = free_stream_mach_number * free_stream_speed_of_sound
print('\n free_sream_mach_number     = ', round(free_stream_mach_number,1))
print(' free_stream_velocity       = ', round(free_stream_velocity,1))

# Computing squares and shortening names
Mi2 = free_stream_mach_number**2
vi2 = free_stream_velocity**2

a_list = []
velocity_list = []

directory = '/media/inigo/10740FB2740F9A1C/Results/12_phd/method/mach1'

for velocity in range(0,814,2):
    velocity_list.append(velocity)
    v2 = velocity**2

    square_brackets_term = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

    local_speed_of_sound_non_dim = np.sqrt(square_brackets_term)
    a_list.append(local_speed_of_sound_non_dim)

    # plt.plot(velocity_list, a_list, label='$M_{\infty}$ = ' + str(round(free_stream_mach_number,2)))
    # plt.grid()
    # axes = plt.gca()
    # axes.set_xlim([0.0, 900])
    # axes.set_ylim([0.0,1.2])

    # filename = directory + '/speed_' + "{:04d}".format(velocity) + '.png'
    # print('filename = ', filename)

    # #save
    # plt.savefig(filename)
    # plt.close()

local_mach_list = []
velocity_list2 = []
a_list = []
ylim = 1.2
for velocity in range(0,814,1):
    velocity_list2.append(velocity)
    v2 = velocity**2

    square_brackets_term = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

    local_speed_of_sound_non_dim = np.sqrt(square_brackets_term)
    a_list.append(local_speed_of_sound_non_dim)

    local_mach = velocity / (free_stream_speed_of_sound * local_speed_of_sound_non_dim)
    local_mach_list.append(local_mach)

    plt.plot(velocity_list2, a_list, label='$M_{\infty}$ = ' + str(round(free_stream_mach_number,2)))
    plt.plot(velocity_list2, local_mach_list, label='$M_{\infty}$ = ' + str(round(free_stream_mach_number,2)))
    plt.grid()
    axes = plt.gca()
    axes.set_xlim([0.0, 900])
    if local_mach > ylim:
        axes.set_ylim([0.0,local_mach])
    else:
        axes.set_ylim([0.0,1.2])

    filename = directory + '/mach_' + "{:03d}".format(velocity) + '.png'
    print('filename = ', filename)

    #save
    plt.savefig(filename)
    plt.close()


# plt.plot(velocity_list, local_mach_list, label='$M_{\infty}$ = ' + str(round(free_stream_mach_number,2)))
# plt.plot(velocity_list, a_list, label='$M_{\infty}$ = ' + str(round(free_stream_mach_number,2)))
# # plt.legend(loc="lower left")
# # plt.xlabel('velocity')
# # plt.ylabel('a')
# plt.grid()
# axes = plt.gca()
# axes.set_xlim([0.0, 900])
# axes.set_ylim([0.0,10.0])
# plt.show()