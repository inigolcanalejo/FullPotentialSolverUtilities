import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

# Input
free_stream_mach_number = 0.72
free_stream_speed_of_sound = 340.3
heat_capacity_ratio = 1.4

hcr = heat_capacity_ratio
print(' free_stream_speed_of_sound = ', free_stream_speed_of_sound)

for free_stream_mach_number in np.arange(0.4, 0.9, 0.1):
    free_stream_velocity = free_stream_mach_number * free_stream_speed_of_sound

    # Computing squares and shortening names
    Mi2 = free_stream_mach_number**2
    vi2 = free_stream_velocity**2

    velocity = np.arange(0., 500.0, 1)

    v2 = velocity**2

    term = 1 + (hcr - 1) / 2 * Mi2 * (1 - v2 / vi2)

    cp = 2.0 / hcr / Mi2 * (pow(term, hcr/(hcr - 1)) - 1)
    cp_i = 1 - v2 / vi2

    print('\n free_sream_mach_number     = ', round(free_stream_mach_number,1))
    print(' free_stream_velocity       = ', round(free_stream_velocity,1))

    #plt.plot(velocity, cp, label='$M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(velocity, cp_i, label='$Incmp. M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))

plt.legend(loc="lower left")
plt.xlabel('velocity')
plt.ylabel('term')
plt.show()