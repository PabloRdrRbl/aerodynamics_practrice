#
# Wind tunel practice data ploting

# import libraries and modules needed
import numpy as np
import matplotlib.pyplot as plt
import os
from plot import plot_voltaje, plot_cp, plot_cla, plot_cp_compared
from calcs import calculate_cp, calculate_cl
from xfoil import get_airfoil_data


if __name__ == "__main__":
    # lab data
    # here my former problem
    # [http://stackoverflow.com/questions/17307299/]
    #
    f = os.path.join(os.path.dirname(__file__), 'data/naca0018lab.csv')
    data = np.loadtxt(f, delimiter=',', dtype=float)
    tunel_data = data[::, :-1:] # not taking p_inff
    inf_data = data[::, -1]


    # offset calibration
    offset = np.amin(tunel_data[1::])
    tunel_data[1::] -= offset
    inf_data -= offset

    # plotting voltages for different AOA
    aoa = [0, 7, 14, 21]

    for i in aoa:
        plot_voltaje(tunel_data[0], tunel_data[aoa.index(i) + 1],
                     tunel_data[aoa.index(i) + 5], i)
        plt.savefig(os.path.join(os.path.dirname(__file__),
                    'plots/voltage-at-aoa{0}'.format(i) + '.png'))


    # plotting cp for different AOA
    aoa = [0, 7, 14, 21]

    for i in aoa:
        cpu, cpl = calculate_cp(tunel_data[aoa.index(i) + 1],
                   tunel_data[aoa.index(i) + 5], inf_data[aoa.index(i) + 5])

        plot_cp(tunel_data[0], cpu, cpl, i)
        plt.savefig(os.path.join(os.path.dirname(__file__),
                    'plots/cp-at-aoa{0}'.format(i) + '.png'))

    # get airfoil data using Xfoil for a given Reynolds number
    re = '5e+5' # choosen Reynolds number, '3.7e+4' is the real estimation
    get_airfoil_data(re)

    # plotting cp vs. alpha
    aoa = [0, 7, 14, 21]
    cl_a = []

    for i in aoa:
        cpu, cpl = calculate_cp(tunel_data[aoa.index(i) + 1],
                   tunel_data[aoa.index(i) + 5], inf_data[aoa.index(i) + 5])
        plot_cp_compared(tunel_data[0], cpu, cpl, i, re)
        cl_a.append(calculate_cl(tunel_data[0], cpu, cpl, i))

    plot_cla(aoa, cl_a, re)
    plt.savefig(os.path.join(os.path.dirname(__file__),
                'plots/cl-alpha' + '.png'))

    # plotting experimental cp compared with numerical
    aoa = [0, 7, 14, 21]

    for i in aoa:
        cpu, cpl = calculate_cp(tunel_data[aoa.index(i) + 1],
                   tunel_data[aoa.index(i) + 5], inf_data[aoa.index(i) + 5])

        plot_cp_compared(tunel_data[0], cpu, cpl, i, re)
        plt.savefig(os.path.join(os.path.dirname(__file__),
                    'plots/comapared-cp-at-aoa{0}'.format(i) + '.png'))

    #plt.show()

#else:
#    plt.ion()
