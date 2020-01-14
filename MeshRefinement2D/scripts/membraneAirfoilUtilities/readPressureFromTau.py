import numpy as np
import re

# TAU's output data file
tau_case = 'Airfoil_Coarse_6deg_SA.Alpha.20'
tau_file_directory = '/media/inigo/10740FB2740F9A1C/SA_Model/' + tau_case
tau_file_directory_aoa = tau_file_directory + '/Airfoil_Coarse_6deg_SA.Gather.SOL'
tau_file_name = tau_file_directory_aoa + '/sol.' + tau_case + '.pval.unsteady_i=200_t=1.00000e00.dat'

print(tau_file_name)

found = False

X = []
Y = []
Z = []
Cp = []

# Read variable
def _read(tau_file, number_of_nodes, variable_list):
    i = 0
    while i < number_of_nodes:
        line = tau_file.readline()
        split = line.split()
        for j in range(len(split)):
            variable_list.append(float(line.split()[j]))
            i +=1

# Skip variable
def _skip(tau_file, number_of_nodes):
    i = 0
    while i < number_of_nodes:
        line = tau_file.readline()
        i +=5

with open(tau_file_name,'r') as tau_file:
    for line in tau_file:
        if 'MEMBRANE' in line:
            line = tau_file.readline()
            header = [int(s) for s in re.findall(r'\b\d+\b', line)]
            number_of_nodes = header[0]

            # Read X
            _read(tau_file, number_of_nodes, X)
            # Skip Y
            _read(tau_file, number_of_nodes, Y)
            # Read Z
            _read(tau_file, number_of_nodes, Z)
            # Skip 13
            for _ in range(13):
                _skip(tau_file, number_of_nodes)
            # Read CP
            _read(tau_file, number_of_nodes, Cp)

# Select only one side
x = []
z = []
cp = []
for i in range(len(Y)):
    if Y[i] > -0.001:
        x.append(X[i])
        z.append(Z[i])
        cp.append(Cp[i])

z_scaled = [i * -10 for i in z]

# Scale and move to fit x from 0 to 1 for the plot
min_x_coordinate = 1e30
max_x_coordinate = -1e30
for i in range(len(x)):
    if(x[i] < min_x_coordinate):
        min_x_coordinate = x[i]
    if(x[i] > max_x_coordinate):
        max_x_coordinate = x[i]

plot_reference_chord_projected = max_x_coordinate - min_x_coordinate
print ('plot_reference_chord_projected = ', plot_reference_chord_projected)

x_plot = []
for i in range(len(x)):
    x_plot.append( (x[i] - min_x_coordinate) / plot_reference_chord_projected )

# Write file
output_file_name = tau_file_directory_aoa + '/cp_tau_aoa_2.dat'

with open(output_file_name, 'w') as output_file:
    for i in range(len(x_plot)):
        output_file.write('{0:15f} {1:15f}\n'.format(x_plot[i], cp[i]))
    output_file.flush()

'''
import matplotlib.pyplot as plt
plt.plot(x_plot, z_scaled, 'b+')
plt.plot(x_plot, cp, 'k*')
#plt.axis('equal')
plt.gca().invert_yaxis()
plt.show()
#'''
