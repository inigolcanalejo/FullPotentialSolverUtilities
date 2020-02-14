import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

# Input
free_stream_mach_number = 0.6
free_stream_speed_of_sound = 340.0
heat_capacity_ratio = 1.4

free_stream_velocity = free_stream_mach_number * free_stream_speed_of_sound
hcr = heat_capacity_ratio
print(' free_stream_speed_of_sound = ', free_stream_speed_of_sound)
print('\n free_sream_mach_number     = ', round(free_stream_mach_number,1))
print(' free_stream_velocity       = ', round(free_stream_velocity,1))

# Computing squares and shortening names
Mi2 = free_stream_mach_number**2
vi2 = free_stream_velocity**2

velocity = 230.0
print(' velocity       = ', round(velocity,1))

v2 = velocity**2

denominator = 1 + (hcr - 1) / 2.0 * Mi2 * (1 - v2 / vi2)

local_mach2 = Mi2 * v2 / (vi2 * denominator)
local_mach = math.sqrt(local_mach2)
print(' local_mach       = ', local_mach)

numerator = local_mach2 * ( 1 + (hcr - 1) / 2.0 * Mi2)
denominator = Mi2 * ( 1 + (hcr -1) / 2.0 * local_mach2)
v2 = vi2 * numerator / denominator
velocity = math.sqrt(v2)

print(' velocity       = ', velocity)

