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
        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)

    def plot(self, x, yu, yl, aoa):
        lines = []

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 15)

        self.ax.set_title('Voltages with $AOA = {0}^\circ$'.format(aoa))
        self.ax.set_xlabel(r'$x/c$ position in the airfoil')
        self.ax.set_ylabel('voltage meassured')

        self.ax.grid()

        l, = self.ax.plot(x, yu, 'bx--', label='upper')
        lines.append(l)
        l, = self.ax.plot(x, yl, 'rx--', label='lower')
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
        self.fig = plt.figure(figsize=(6, 7), dpi=100)

        c = 0.05
        self.left, self.width = 0.15 , 0.8
        self.rect1 = [self.left, 0.3+c, self.width, 0.6-c]
        self.rect2 = [self.left, 0.05, self.width, 0.2+c]

        axprops = dict(xticks=[], yticks=[])
        self.ax1 = self.fig.add_axes(self.rect1)
        self.ax2 = self.fig.add_axes(self.rect2, sharex=self.ax1, **axprops)

    def plot(self, x, cpu, cpl, aoa):
        lines = []

        # load geometry from data file
        # data generated using naca.py
        # https://github.com/dgorissen/naca
        #
        xg, yg = np.loadtxt(os.path.join(os.path.dirname(__file__),
                             'data/naca0018-geometry.dat'), delimiter=' ').T

        self.ax1.set_xlim(0, 1)
        self.ax1.set_ylim(1, -4)

        self.ax1.set_title("$C_{p}$ at $AOA = %s^\circ$" % (aoa))
        self.ax1.set_ylabel('$C_{p}$')
        self.ax1.set_xlabel(r'$x/c$ position in the airfoil')
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

        l, = self.ax1.plot(x, cpu, 'bx--', label='upper')
        lines.append(l)
        l, = self.ax1.plot(x, cpl, 'rx--', label='lower')
        lines.append(l)

        l, = self.ax2.plot((xg[300::] + 0.01) * 0.99, yg[300::] * 0 - 1,
                           color='k', linestyle='--', linewidth=1.5)
        lines.append(l)
        # index 300 is (0.0, 0.0)
        l, = self.ax2.plot((xg[:301:] + 0.01) * 0.99, yg[:301:] - 1,
                           color='b', linestyle='-', linewidth=1.5)
        lines.append(l)
        l, = self.ax2.plot((xg[300::] + 0.01) * 0.99, yg[300::] - 1,
                           color='r', linestyle='-', linewidth=1.5)
        lines.append(l)

        self.ax1.legend(loc='upper right')

        return lines

def calculate_cl(x, cpu, cpl, aoa):
    # not dividing by c because it's x/c realy
    # doing cl = cn * cos(aoa)
    cl = (np.trapz(cpl, x) - np.trapz(cpu, x)) * np.cos(aoa * np.pi / 180)

    return cl

def plot_cla(aoa, cl):
    p = ClaPlot()
    return p.plot(aoa, cl)

class ClaPlot(object):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)

    def plot(self, aoa, cl):
        lines = []

        f = os.path.join(os.path.dirname(__file__), 'data/cla_data.csv')
        data_atools = np.loadtxt(f, dtype=float).T

        # least squares courve fitting
        xx = np.linspace(-5, 22, 300)
        z = np.polyfit(aoa, cl, 3)
        # it is convenient to use poly1d objects for dealing with polynomials
        p = np.poly1d(z)

        self.ax.set_ylim(-0.5, 1.7)
        self.ax.set_xlim(-5, 22)

        self.ax.set_title(r'$c_{l}-\alpha$')
        self.ax.set_xlabel('Angle of attack')
        self.ax.set_ylabel(r'$c_{l}$')

        self.ax.grid()

        l, = self.ax.plot(xx, p(xx), 'g-')
        lines.append(l)
        l, = self.ax.plot(aoa, cl, 'o', label='experimental $c_{l}$')
        lines.append(l)
        l, = self.ax.plot(data_atools[0], data_atools[1], 'k--',
                          label=r'numerical $Re = 3e+6$')
        lines.append(l)

        self.ax.legend(loc='lower right')

        return lines

def plot_cp_compared(x, cpu, cpl, aoa):
    p = ComparedPlot()
    return p.plot(x, cpu, cpl, aoa)

class ComparedPlot(object):

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 7), dpi=100)

    def plot(self, x, cpu, cpl, aoa):
        lines = []

        # now we compare reference (numerical) data with the experimental ones
        # data taken from Xfoil
        f = os.path.join(os.path.dirname(__file__),
                         'aux_data/naca0018-cpx-aoa{}.txt'.format(aoa))
        numerical_data = np.loadtxt(f, dtype=float).T

        aoa_list = [0, 7, 14, 21]

        cpu, cpl = calculate_cp(tunel_data[aoa_list.index(aoa) + 1],
                    tunel_data[aoa_list.index(aoa) + 5],
                               inf_data[aoa_list.index(aoa) + 5])

        self.ax.set_xlim(0.0, 1.0)
        if aoa == 0:
            self.ax.set_ylim(-4, 1.5)
        else:
            self.ax.set_ylim(np.amin(numerical_data[1]) - 0.3, 1.5)

        self.ax.set_title("Theorical $C_{p}$ with $AOA = %d^\circ$ vs. data"
                          % (aoa))
        self.ax.set_xlabel(r'$x/c$ position in the airfoil')
        self.ax.set_ylabel('$C_{p}$')

        self.ax.invert_yaxis()

        #self.ax.grid()

        l, = self.ax.plot(tunel_data[0], cpu, 'bx--', markersize=8,
                          label='upper')
        lines.append(l)
        l, = self.ax.plot(tunel_data[0], cpl, 'rx--', markersize=8,
                          label='lower')
        lines.append(l)

        ii = int(numerical_data.shape[1] / 2)
        l, = self.ax.plot(numerical_data[0, ii::], numerical_data[1, ii:0:-1],
                          color='k', linestyle='-', linewidth=0.5,
                          label=r'numerical at $Re = Inviscous$')
        lines.append(l)
        l, = self.ax.plot(numerical_data[0, ii::], numerical_data[1, ii::],
                          color='k', linestyle='-', linewidth=0.5)
        lines.append(l)
        l, = self.ax.plot(numerical_data[0, ii::], numerical_data[1, ii::]*0+1,
                          color='g', linestyle='--', linewidth=2,
                          label='stagnation point')
        lines.append(l)

        self.ax.legend(loc='upper right')

        return lines

if __name__ == "__main__":
    # lab data
    # here my former problem
    # http://stackoverflow.com/questions/17307299/
    #
    f = os.path.join(os.path.dirname(__file__), 'data/naca0018lab.csv')
    data = np.loadtxt(f, delimiter=',', dtype=float)
    tunel_data = data[::, :-1:] # not taking p_inff
    inf_data = data[::, -1]


    # offset calibration
    offset = np.amin(tunel_data[1::])
    tunel_data[1::] -= offset
    inf_data -= offset


    # plotting voltages and cp for different AOA
    aoa = [0, 7, 14, 21]

    for i in aoa:
        plot_voltaje(tunel_data[0], tunel_data[aoa.index(i) + 1],
                     tunel_data[aoa.index(i) + 5], i)
        plt.savefig(os.path.join(os.path.dirname(__file__),
                    'plots/voltage-at-aoa{0}'.format(i) + '.png'))


    # plotting voltages and cp for different AOA
    aoa = [0, 7, 14, 21]

    for i in aoa:
        cpu, cpl = calculate_cp(tunel_data[aoa.index(i) + 1],
                   tunel_data[aoa.index(i) + 5], inf_data[aoa.index(i) + 5])

        plot_cp(tunel_data[0], cpu, cpl, i)
        plt.savefig(os.path.join(os.path.dirname(__file__),
                    'plots/cp-at-aoa{0}'.format(i) + '.png'))


    # plotting cp vs. alpha
    aoa = [0, 7, 14, 21]
    cl_a = []

    for i in aoa:
        cpu, cpl = calculate_cp(tunel_data[aoa.index(i) + 1],
                   tunel_data[aoa.index(i) + 5], inf_data[aoa.index(i) + 5])
        cl_a.append(calculate_cl(tunel_data[0], cpu, cpl, i))

    plot_cla(aoa, cl_a)
    plt.savefig(os.path.join(os.path.dirname(__file__),
                'plots/cl-alpha' + '.png'))

    # plotting experimental cp compared with numerical one at Re=3e+5
    aoa = [0, 7, 14, 21]

    for i in aoa:
        cpu, cpl = calculate_cp(tunel_data[aoa.index(i) + 1],
                   tunel_data[aoa.index(i) + 5], inf_data[aoa.index(i) + 5])

        plot_cp_compared(tunel_data[0], cpu, cpl, i)
        plt.savefig(os.path.join(os.path.dirname(__file__),
                    'plots/comapared-cp-at-aoa{0}'.format(i) + '.png'))

    #plt.show()

#else:
#    plt.ion()
