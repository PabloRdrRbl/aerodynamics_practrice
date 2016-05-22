#
# Wind tunel practice calculations

# import libraries and modules needed
import numpy as np
from scipy import integrate, linalg


def calculate_cp(yu, yl, y_inf):
    cpu = 1 - (yu / y_inf)
    cpl = 1 - (yl / y_inf)

    return cpu, cpl

def calculate_cl(x, cpu, cpl, aoa):
    # not dividing by c because it's x/c realy
    # doing cl = cn * cos(aoa)
    cl = (np.trapz(cpl, x) - np.trapz(cpu, x)) * np.cos(aoa * np.pi / 180)

    return cl
