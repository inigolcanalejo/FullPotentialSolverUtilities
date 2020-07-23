import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

# 1° Compute the critical pressure coefficient for different mach numbers

# Definning gamma
heat_capacity_ratio = 1.4
hcr = heat_capacity_ratio

# Definning range of free stream mach numbers
minimum_free_stream_mach = 0.05
maximum_free_stream_mach = 1.0
free_stream_mach_number = np.arange(minimum_free_stream_mach, maximum_free_stream_mach, 0.001)

# Computing squares and shortening names
Mi2 = free_stream_mach_number**2

# Applying formula 8.169 from FVA
term = (1 + (hcr - 1) / 2 * Mi2) / (1 + (hcr - 1) / 2)
cp_crit = 2.0 / hcr / Mi2 * (pow(term, hcr/(hcr - 1)) - 1)

# 2° Compute the minimum pressure coefficient for different mach number:
cpi_min = -0.610745
cp_min = cpi_min / np.sqrt(1 - Mi2)

# Initialize variables for the search
critical_mach_number = 0.0
diference = 1e3
index = 0

# Loop over the values and find the closest ones
# i.e. finding the critical mach number
for i in range(len(cp_min)):
    if abs(cp_min[i]-cp_crit[i]) < diference:
        critical_mach_number = free_stream_mach_number[i]
        diference = abs(cp_min[i]-cp_crit[i])
        index = i

# Print found values
print('Critical mach number = ', round(critical_mach_number,4))
print('cp_crit = ', round(cp_crit[index],4))
print('cp_min = ', round(cp_min[index],4))
print('difference = ', round(diference,4))

# Plot values:
yrange = np.arange(-2, 0, 0.01)
critical_mach_number_array = np.full((len(yrange)),critical_mach_number)
plt.plot(free_stream_mach_number, cp_crit, label='$c_p^*$')
plt.plot(free_stream_mach_number, cp_min, label='$c_{pmin}$')
plt.plot(critical_mach_number_array, yrange, 'k--', label='$M_{\infty}^*$ = ' + str(round(critical_mach_number,3)))

plt.legend(loc="lower left")
plt.xlabel('$M_{\infty}$')
plt.ylabel('$c_p$')
axes = plt.gca()
axes.set_xlim([minimum_free_stream_mach, maximum_free_stream_mach])
axes.set_ylim([-2,0])
plt.gca().invert_yaxis()
plt.show()