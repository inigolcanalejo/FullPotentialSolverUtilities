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

free_stream_mach_number = 0.85
free_stream_speed_of_sound = 340.0
free_streem_velocity = free_stream_mach_number*free_stream_speed_of_sound

vi2 = free_streem_velocity**2
Mi2 = free_stream_mach_number**2

vacuum_speed2 = vi2 * (1 + 2 / ((hcr-1)*Mi2))
vacuum_speed = math.sqrt(vacuum_speed2)

print('free_stream_mach_number = ', free_stream_mach_number)
print('free_stream_speed_of_sound = ', free_stream_speed_of_sound)
print('free_streem_velocity = ', free_streem_velocity)
print('vacuum_speed = ', vacuum_speed)

