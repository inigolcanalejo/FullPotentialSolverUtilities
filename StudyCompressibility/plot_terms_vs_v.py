import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

# Input
free_stream_speed_of_sound = 340.0
heat_capacity_ratio = 1.4
free_stream_density = 1.0

hcr = heat_capacity_ratio
ai2 = free_stream_speed_of_sound * free_stream_speed_of_sound
print(' free_stream_speed_of_sound = ', free_stream_speed_of_sound)

for free_stream_mach_number in np.arange(0.8, 1.3, 1):
    free_stream_velocity = free_stream_mach_number * free_stream_speed_of_sound

    # Computing squares and shortening names
    Mi2 = free_stream_mach_number**2
    vi2 = free_stream_velocity**2

    velocity = np.arange(000., 400.0, 1.0)

    v2 = velocity**2

    square_brackets_term = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

    density = free_stream_density * pow(square_brackets_term, 1/(hcr-1))

    term_2 = pow(square_brackets_term, (2-hcr)/(hcr-1)) * v2 / ai2

    print('\n free_sream_mach_number     = ', round(free_stream_mach_number,1))
    print(' free_stream_velocity       = ', round(free_stream_velocity,1))

    plt.plot(velocity, density, label='term 1 $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(velocity, term_2,  label='term 2 $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(velocity, density - term_2, label='Difference $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))

plt.legend(loc="lower left")
plt.xlabel('velocity')
plt.ylabel('term')
plt.grid()
plt.show()