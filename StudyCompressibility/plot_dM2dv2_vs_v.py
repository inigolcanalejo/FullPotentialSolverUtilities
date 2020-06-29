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

    velocity = np.arange(0.0, 700.0, 1.0)

    v2 = velocity**2

    square_brackets_term = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

    local_mach2 = Mi2 * v2 / (vi2 * square_brackets_term)
    local_mach = np.sqrt(local_mach2)

    dM2_dq2 = local_mach2 * (1/v2 + (hcr - 1) * Mi2 / (2.0 * vi2 * square_brackets_term))

    dM2_dq2_2 = Mi2 / vi2 * (1 + (hcr - 1) / 2.0 * Mi2) / square_brackets_term**2

    # checking the formulas using finite differences
    delta = v2 / v2 * 1e-1

    print(' delta       = ', v2[400])
    v2 += delta
    square_brackets_term = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

    local_mach2_plus = Mi2 * v2 / (vi2 * square_brackets_term)

    v2 -= 2*delta
    square_brackets_term = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

    local_mach2_minus = Mi2 * v2 / (vi2 * square_brackets_term)

    dM2_dq2_fd = 0.5 * (local_mach2_plus - local_mach2_minus) / 1e-1

    difference = dM2_dq2_fd - dM2_dq2

    print('\n free_sream_mach_number     = ', round(free_stream_mach_number,1))
    print(' free_stream_velocity       = ', round(free_stream_velocity,1))
    print(' delta       = ', v2[400])

    plt.plot(local_mach, dM2_dq2, label='$M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(local_mach, dM2_dq2_2, label='2$M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(local_mach, dM2_dq2_fd, label='fd$M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(local_mach, difference, label='diff$M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))

plt.legend(loc="upper left")
plt.xlabel('local mach')
plt.ylabel('dM2/dq2')
plt.grid()
plt.show()