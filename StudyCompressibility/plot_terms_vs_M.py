import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

def ComputeUpwindingFactor(mach_number):
    m2 = mach_number * mach_number
    upwinding_factor = 1 - 0.99**2 / m2
    for i in range(upwinding_factor.size):
        if upwinding_factor[i] < 0.0:
            upwinding_factor[i] = 0.0
    return upwinding_factor

# Input
free_stream_speed_of_sound = 340.0
heat_capacity_ratio = 1.4
free_stream_density = 1.225

hcr = heat_capacity_ratio
ai2 = free_stream_speed_of_sound * free_stream_speed_of_sound
print(' free_stream_speed_of_sound = ', free_stream_speed_of_sound)

for free_stream_mach_number in np.arange(0.8, 0.85, 1):
    free_stream_velocity = free_stream_mach_number * free_stream_speed_of_sound

    # Computing squares and shortening names
    Mi2 = free_stream_mach_number**2
    vi2 = free_stream_velocity**2

    velocity = np.arange(1., 600.0, 1.0)

    v2 = velocity**2

    square_brackets_term = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

    density = free_stream_density * pow(square_brackets_term, 1/(hcr-1))
    Ddensity_Dv2 = free_stream_density * pow(square_brackets_term, (2-hcr)/(hcr-1)) / (2 * ai2)
    term_2 = 2 * Ddensity_Dv2 * v2

    local_mach2 = Mi2 * v2 / (vi2 * square_brackets_term)
    local_mach = np.sqrt(local_mach2)

    # Compute modified terms for comparison:
    upwinding_factor = ComputeUpwindingFactor(local_mach)

    density_diference = np.zeros(density.size)
    density_mod = np.zeros(density.size)
    for i in range(0, 4):
        density_mod[i] = density[i] - upwinding_factor[i]*(density[i] - density[i-1])
        density_diference[i] = upwinding_factor[i]*(density[i] - density[i-1])
    for i in range(4, density.size):
        density_mod[i] = density[i] - upwinding_factor[i]*(density[i] - density[i-1])
        density_diference[i] = upwinding_factor[i]*(density[i] - density[i-1])

    # Compute nonlinear term modified
    Dmu_DM2 = np.zeros(density.size)
    for i in range(density.size):
        if local_mach[i] > 1.0:
            Dmu_DM2[i] = 0.99**2 / local_mach[i]**4

    dM2_dv2 = local_mach2 * (1/v2 + (hcr - 1) * Mi2 / (2.0 * vi2 * square_brackets_term))
    term_2_mod = 2 * v2 * (Ddensity_Dv2 * (1 - upwinding_factor) - Dmu_DM2 * dM2_dv2)
    factor = Dmu_DM2 * dM2_dv2
    term_diff_mod = density_mod - term_2_mod

    print('\n free_sream_mach_number     = ', round(free_stream_mach_number,1))
    print(' free_stream_velocity       = ', round(free_stream_velocity,1))

    plt.plot(local_mach, density, label='term 1 $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(local_mach, term_2,  label='term 2 $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    plt.plot(local_mach, density - term_2, label='Difference $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    #plt.plot(local_mach, upwinding_factor,  label='upwinding factor $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    #plt.plot(local_mach, density_mod,  label='term 1 mod $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    #plt.plot(local_mach, density_diference,  label='density diference $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    #plt.plot(local_mach, Dmu_DM2,  label='Dmu DM2 $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    #plt.plot(local_mach, dM2_dv2,  label='dM2dq2 $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    #plt.plot(local_mach, term_2_mod,  label='term 2 mod $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))
    #plt.plot(local_mach, term_diff_mod,  label='difference mod $M_{\infty}$ = ' + str(round(free_stream_mach_number,1)))

plt.legend(loc="lower left")
plt.xlabel('local mach')
plt.ylabel('density')
plt.grid()
plt.show()