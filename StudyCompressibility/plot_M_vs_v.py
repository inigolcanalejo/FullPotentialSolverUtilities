import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

# Input
free_stream_speed_of_sound = 340.0
heat_capacity_ratio = 1.4

hcr = heat_capacity_ratio
ai2 = free_stream_speed_of_sound * free_stream_speed_of_sound
print(' free_stream_speed_of_sound = ', free_stream_speed_of_sound)

for free_stream_mach_number in np.arange(0.8, 0.85, 0.3):
    free_stream_velocity = free_stream_mach_number * free_stream_speed_of_sound

    # Computing squares and shortening names
    Mi2 = free_stream_mach_number**2
    vi2 = free_stream_velocity**2

    velocity = np.arange(0.0, 1500.0, 1.0)

    v2 = velocity**2

    square_brackets_term = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

    local_mach2 = Mi2 * v2 / (vi2 * square_brackets_term)
    local_mach = np.sqrt(local_mach2)
    speed_of_sound_squared = vi2 * square_brackets_term / Mi2

    vacuum_speed = np.sqrt(vi2 * (1 + 2 / ((hcr - 1)*Mi2)))

    print('\n free_sream_mach_number     = ', round(free_stream_mach_number,1))
    print(' free_stream_velocity       = ', round(free_stream_velocity,1))
    print(' vacuum_speed       = ', round(vacuum_speed,1))

    #plt.plot(velocity, local_mach, label='$M$')
    #plt.plot(velocity, local_mach2, label='$M^2$')
    plt.plot(velocity, v2, label='$v^2$')
    #plt.plot(velocity, speed_of_sound_squared, label='$a^2$')

plt.legend(loc="upper left")
plt.xlabel('velocity magnitude [m/s]')
plt.ylabel('velocity magnitude squared [$m^2/s^2$]')
plt.xlim([0, 1600])
plt.grid()
plt.show()