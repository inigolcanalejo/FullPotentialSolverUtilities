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
free_stream_mach_number = 0.84

# Computing squares and shortening names
Mi2 = free_stream_mach_number**2

# Applying formula 8.169 from FVA
term = (1 + (hcr - 1) / 2 * Mi2) / (1 + (hcr - 1) / 2)
cp_crit = 2.0 / hcr / Mi2 * (pow(term, hcr/(hcr - 1)) - 1)

# self.critical_cp = (math.pow((1+(self.hcr-1)*self.free_stream_mach**2/2)/(
#             1+(self.hcr-1)/2), self.hcr/(self.hcr-1)) - 1) * 2 / (self.hcr * self.free_stream_mach**2)

# Print found values
print('Critical cp = ', round(cp_crit,4))

free_stream_mach_number = np.arange(0.1, 10.0, 0.1)

# Computing squares and shortening names
Mi2 = free_stream_mach_number**2

# Applying formula 8.169 from FVA
term = (1 + (hcr - 1) / 2 * Mi2) / (1 + (hcr - 1) / 2)
cp_crit = 2.0 / hcr / Mi2 * (pow(term, hcr/(hcr - 1)) - 1)

plt.plot(free_stream_mach_number, cp_crit)
plt.xlabel('Mach number')
plt.ylabel('Critical pressure coefficient')
plt.grid()
plt.show()

