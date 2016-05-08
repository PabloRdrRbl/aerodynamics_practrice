#
# Wind tunel practice data ploting

# import libraries and modules needed
import numpy as np
from scipy import integrate, linalg
import matplotlib
from matplotlib import pyplot as plt
import os

# customizing plots
plt.style.use('classic')

def plot_voltaje(x, yu, yl, aoa):
    v = VoltagePlot()
    return v.plot(x, yu, yl, aoa)

class VoltagePlot(object):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)

    def plot(self, x, yu, yl, aoa):
        lines = []

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 17)

        self.ax.set_title('Voltages with $AOA = {0}^\circ$'.format(aoa))
        self.ax.set_xlabel('x position in the airfoil')
        self.ax.set_ylabel('voltage meassured')

        self.ax.grid()

        l, = self.ax.plot(x, yu, 'b.--', label='upper')
        lines.append(l)

        l, = self.ax.plot(x, yl, 'r.--', label='lower')
        lines.append(l)

        self.ax.legend(loc='lower right')

        return lines

def calculate_cp(yu, yl, y_inf):
    cpu = 1 - (yu / y_inf)
    cpl = 1 - (yl / y_inf)
    return cpu, cpl

def plot_cp(x, cpu, cpl, aoa):
    cp = CpPlot()
    return cp.plot(x, cpu, cpl, aoa)

class CpPlot(object):
    def __init__(self):
        self.fig = plt.figure(figsize=(6, 4), dpi=100)

        c = 0.05
        self.left, self.width = 0.15 , 0.8
        self.rect1 = [self.left, 0.3+c, self.width, 0.6-c]
        self.rect2 = [self.left, 0.05, self.width, 0.2+c]

        axprops = dict(xticks=[], yticks=[])
        self.ax1 = self.fig.add_axes(self.rect1)
        self.ax2 = self.fig.add_axes(self.rect2, sharex=self.ax1, **axprops)

    def plot(self, x, cpu, cpl, aoa):
        # load geometry from data file
        # data generated using naca.py
        # https://github.com/dgorissen/naca
        #
        xg, yg = np.loadtxt(os.path.join(os.path.dirname(__file__),
                             'data/naca0018-geometry.dat'), delimiter=' ').T

        self.ax1.set_xlim(0, 1)
        self.ax1.set_ylim(1, -3)

        self.ax1.set_title("$C_{p}$ with $AOA = %s^\circ$" % (aoa))
        self.ax1.set_ylabel('$C_{p}$')
        self.ax1.set_xticks(np.arange(0, 11, 2)/10)
        self.ax2.set_xticklabels(np.arange(0, 11, 2)/10)


        self.ax1.grid()

        self.ax2.set_aspect('equal')
        self.ax2.spines['right'].set_visible(False)
        self.ax2.spines['left'].set_visible(False)
        self.ax2.spines['bottom'].set_visible(False)
        self.ax2.spines['top'].set_visible(False)
        self.ax2.set_xticklabels([])
        self.ax2.set_yticklabels([])
        self.ax2.get_xaxis().set_visible(False)
        self.ax2.get_yaxis().set_visible(False)

        self.ax1.plot(x, cpu, 'b.--', label='upper')
        self.ax1.plot(x, cpl, 'r.--', label='lower')

        # index 300 is (0.0, 0.0)
        self.ax2.plot(xg[:301:], yg[:301:]-1, color='b', linestyle='-', linewidth=1)
        self.ax2.plot(xg[300::], yg[300::]-1, color='r', linestyle='-', linewidth=1)

        self.ax1.legend(loc='upper right')


if __name__ == "__main__":
    # lab data
    # here my former problem
    # http://stackoverflow.com/questions/17307299/
    # filling-missing-values-using-numpy-genfromtxt
    #
    f = os.path.join(os.path.dirname(__file__), 'data/naca0018lab.csv')
    data = np.loadtxt(f, delimiter=',', dtype=float)
    tunel_data = data[::, :-1:]
    inf_data = data[::, -1]

    # plotting voltages and cp for different AOA
    l = [0, 7, 14, 21]

    for i in l:
        plot_voltaje(tunel_data[0], tunel_data[l.index(i) + 1],
                     tunel_data[l.index(i) + 5], i)
        plt.savefig(os.path.join(os.path.dirname(__file__),
                    'plots/voltage-at-aoa{0}'.format(i) + '.png'))

    for i in l:
        cpu, cpl = calculate_cp(tunel_data[l.index(i) + 1],
                   tunel_data[l.index(i) + 5], inf_data[l.index(i) + 5])

        plot_cp(tunel_data[0], cpu, cpl, i)
        plt.savefig(os.path.join(os.path.dirname(__file__),
                    'plots/cp-at-aoa{0}'.format(i) + '.png'))

    #############################################
    # now we compare reference data with the experimental ones
    # data taken from
    # Abbot and von Doenhoff, "Theory of Wing Sections," 1949 data
    # page 325m, NACA 0018 cp for aoa = 0
    f = os.path.join(os.path.dirname(__file__), 'data/naca0018at0-theo.csv')
    data = np.loadtxt(f, delimiter=',', dtype=float)
    xtheo = data[0] / 100 # we what them to be betweet 0 and 1
    voverVsquared = data[1]

    cp = 1 - voverVsquared

    l = [0, 7, 14, 21]
    i = 0

    cpu, cpl = calculate_cp(tunel_data[l.index(i) + 1],
                tunel_data[l.index(i) + 5], inf_data[l.index(i) + 5])

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-3, 1.3)

    ax.set_title("Theorical $C_{p}$ with $AOA = 0^\circ$ vs. data")
    ax.set_xlabel('x position in the airfoil')
    ax.set_ylabel('$C_{p}$')

    ax.invert_yaxis()

    ax.grid()

    ax.plot(tunel_data[0], cpu, 'b.--', label='upper')
    ax.plot(tunel_data[0], cpl, 'r.--', label='lower')
    ax.plot(xtheo, cp, 'kx--', label='theo')

    ax.legend(loc='upper right')

    plt.savefig(os.path.join(os.path.dirname(__file__),
                'plots/compared-cp-at-aoa{0}'.format(i) + '.png'))

    #############################################
    # now we compare reference data with the experimental ones
    # data taken from XFoil
    f = os.path.join(os.path.dirname(__file__), 'data/naca0018at7.cp')
    data_lol = np.loadtxt(f, delimiter=',', dtype=float).T

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-3, 1.3)

    ax.set_title("Theorical $C_{p}$ with $AOA = 7^\circ$ vs. data")
    ax.set_xlabel('x position in the airfoil')
    ax.set_ylabel('$C_{p}$')

    ax.invert_yaxis()

    ax.grid()

    ax.plot(tunel_data[0], cpu, 'b.--', label='upper')
    ax.plot(tunel_data[0], cpl, 'r.--', label='lower')

    l = [0, 7, 14, 21]
    i = 0

    ii = int(data_lol.shape[1] / 2)
    ax.plot(data_lol[0, ii::], data_lol[1, ii:0:-1], 'k--', label='theo')
    ax.plot(data_lol[0, ii::], data_lol[1, ii::], 'k--')

    ax.legend(loc='upper right')

    plt.savefig(os.path.join(os.path.dirname(__file__),
                'plots/ccompared-cp-at-aoa{0}'.format(i) + '.png'))

    plt.show()

#else:
#    plt.ion()
