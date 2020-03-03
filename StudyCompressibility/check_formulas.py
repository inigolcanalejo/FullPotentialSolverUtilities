# Maximum displacement

# 210°
print('\n210°')
h = 240.8   # Height
b = 117.0   # Building width [m]
K = 0.13    # Effective correlation length factor [-]
K_w = 5.03  # Mode shape factor [-]
c_lat = 1.1 # Lateral force coefficient [-]
St = 0.12   # Strouhal number [-]
Sc = 1.499  # Scruton number [-]

# # Scruton Number
# damping = 0.05
# m = 251434.37
# density = 1.25
# Sc = 2 * damping * m / (density * b**2)
# print('\nSc = ', Sc)

# Effective correlation length factor
Lj_b = 12
#b_2 = 52.0
slenderness = 4.6
slenderness = h / b
print('\nslenderness = ', slenderness)
r = Lj_b / slenderness
K_w = 3 * r * (1 - r + r**2 / 3.0)
print('\nK_w = ', K_w)

y_max = b * K * K_w * c_lat / (St**2 * Sc)
#y_max /= b
print('\ny_max = ', y_max)

# 315°
print('\n315°')
b = 34.0    # Building width [m]
K = 0.13    # Effective correlation length factor [-]
K_w = 85.15  # Mode shape factor [-]
c_lat = 1.1 # Lateral force coefficient [-]
St = 0.15   # Strouhal number [-]
Sc = 17.76  # Scruton number [-]

# Scruton Number
# damping = 0.05
# m = 251434.37
# density = 1.25
# Sc = 2 * damping * m / (density * b**2)
print('\nSc = ', Sc)

# Effective correlation length factor
Lj_b = 12
#b_2 = 108
slenderness = 2.2
slenderness = h / b
print('\nslenderness = ', slenderness)
r = Lj_b / slenderness
K_w = 3 * r * (1 - r + r**2 / 3.0)
print('\nK_w = ', K_w)


y_max = b * K * K_w * c_lat / (St**2 * Sc)
#y_max /= b
print('\ny_max = ', y_max)


import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

for Lj_b in np.arange(2.0, 14.0, 2):

    slenderness = np.arange(2., 10.0, 0.1)
    r = Lj_b / slenderness
    K_w = 3 * r * (1 - r + r**2 / 3.0)

    plt.plot(slenderness, K_w, label='$L_j/b$ = ' + str(round(Lj_b,1)))

plt.legend(loc="upper right")
plt.xlabel('Slenderness $\lambda$')
plt.ylabel('Correlation length factor $K_w$')
plt.title('Correlation length factor $(K_w)$ vs Slenderness $(\lambda)$ for different correlation lengths $(L_j/b)$ $(3\cdot \\frac{L_j/b}{\lambda}[1-\\frac{L_j/b}{\lambda} + \\frac{1}{3}\cdot(\\frac{L_j/b}{\lambda})^2])$')
plt.grid()
plt.show()