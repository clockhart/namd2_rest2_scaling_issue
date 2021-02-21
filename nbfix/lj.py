
import numpy as np

r = 1.46
e_min = 0.083875
r_min = 3.731 

energy = e_min * (np.power(r_min / r, 12) - 2. * np.power(r_min / r, 6))

print(f'unscaled = {energy}')
print(f'scaled = {energy / 2.}')


