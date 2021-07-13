import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

directory = '/media/inigo/10740FB2740F9A1C/Results/12_phd/method/terms_dat'
def WritePlotToFile(file_name, x, y):
    with open(file_name, 'w') as file_write:
        for i in range(len(x)):
            file_write.write('{0:15f} {1:15f}\n'.format(x[i], y[i]))

# Input
free_stream_speed_of_sound = 340.0
heat_capacity_ratio = 1.4
free_stream_density = 1.0

hcr = heat_capacity_ratio
ai2 = free_stream_speed_of_sound * free_stream_speed_of_sound
print(' free_stream_speed_of_sound = ', free_stream_speed_of_sound)

for free_stream_mach_number in np.arange(0.8, 0.85, 1):
    free_stream_velocity = free_stream_mach_number * free_stream_speed_of_sound

    # Computing squares and shortening names
    Mi2 = free_stream_mach_number**2
    vi2 = free_stream_velocity**2

    velocity = np.arange(000., 400.0, 1.0)

    v2 = velocity**2

    square_brackets_term = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

    density = free_stream_density * pow(square_brackets_term, 1/(hcr-1))

    term_2 = pow(square_brackets_term, (2-hcr)/(hcr-1)) * v2 / ai2

    local_mach2 = Mi2 * v2 / (vi2 * square_brackets_term)
    local_mach = np.sqrt(local_mach2)

    print('\n free_sream_mach_number     = ', round(free_stream_mach_number,1))
    print(' free_stream_velocity       = ', round(free_stream_velocity,1))

    filename = directory + '/term1.dat'
    WritePlotToFile(filename, local_mach, density)

    filename = directory + '/term2.dat'
    WritePlotToFile(filename, local_mach, term_2)

    filename = directory + '/jacobian.dat'
    WritePlotToFile(filename, local_mach, density - term_2)

    plt.plot(local_mach, density, label='term 1 $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(local_mach, term_2,  label='term 2 $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(local_mach, density - term_2, label='Difference $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))

plt.legend(loc="lower left")
plt.xlabel('local mach')
plt.ylabel('density')
plt.grid()
plt.show()