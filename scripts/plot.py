#
# Wind tunel practice data ploting
#

# import libraries and modules needed
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import os
from calcs import calculate_cp, calculate_cl

# customizing plots
#plt.style.use('classic')

def plot_voltaje(x, yu, yl, aoa):
    v = VoltagePlot()
    return v.plot(x, yu, yl, aoa)

class VoltagePlot(object):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=10000)

    def plot(self, x, yu, yl, aoa):
        lines = []

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 15)

        self.ax.set_title('Voltages with $AOA = {0}^\circ$'.format(aoa))
        self.ax.set_xlabel(r'$x/c$')
        self.ax.set_ylabel('voltage meassured (calibrated)')

        self.ax.grid()

        l, = self.ax.plot(x, yu, 'bx--', label='upper')
        lines.append(l)
        l, = self.ax.plot(x, yl, 'rx--', label='lower')
        lines.append(l)


        self.ax.legend(loc='lower right')

        return lines

def plot_cp(x, cpu, cpl, aoa):
    cp = CpPlot()
    return cp.plot(x, cpu, cpl, aoa)

class CpPlot(object):
    def __init__(self):
        self.fig = plt.figure(figsize=(6, 7), dpi=10000)

        c = 0.05
        self.left, self.width = 0.15 , 0.8
        self.rect1 = [self.left, 0.3+c, self.width, 0.6-c]
        self.rect2 = [self.left, 0.05, self.width, 0.2+c]

        self.axprops = dict(xticks=[], yticks=[])
        self.ax1 = self.fig.add_axes(self.rect1)
        self.ax2 = self.fig.add_axes(self.rect2, sharex=self.ax1, **self.axprops)

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

        self.ax1.set_title("Experimental $C_{p}$ at $AOA = %s^\circ$" % (aoa))
        self.ax1.set_ylabel('$C_{p}$')
        self.ax1.set_xlabel(r'$x/c$')

        self.ax1.set_xticks(np.arange(0, 11, 2)/10)
        self.ax1.grid()

        self.ax2.set_xticklabels(np.arange(0, 11, 2)/10)

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

def plot_cla(aoa, cl, re):
    p = ClaPlot()
    return p.plot(aoa, cl, re)

class ClaPlot(object):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=10000)

    def plot(self, aoa, cl, re):
        lines = []

        f = os.path.join(os.path.dirname(__file__),
                         'data/cla-data/naca0018-cla-re{0}.txt'.format(re))
        data_atools = np.loadtxt(f, dtype=float).T

        # least squares courve fitting
        xx = np.linspace(-5, 22, 300)
        z = np.polyfit(aoa, cl, 3)
        # it is convenient to use poly1d objects for dealing with polynomials
        p = np.poly1d(z)

        self.ax.set_ylim(-0.5, 1.7)
        self.ax.set_xlim(-5, 22)

        self.ax.set_title(r'$c_{l}-\alpha$ numerical vs. experimental data')
        self.ax.set_xlabel('Angle of attack')
        self.ax.set_ylabel(r'$c_{l}$', size=15)

        self.ax.grid()

        l, = self.ax.plot(xx, p(xx), 'g-', linewidth=3)
        lines.append(l)
        l, = self.ax.plot(xx, 2 * np.pi * xx * np.pi / 180  , 'r--',
                          linewidth=2,
                          label=r'theoretical $(c_{l}=2\pi\alpha)$')
        lines.append(l)
        l, = self.ax.plot(data_atools[0], data_atools[1], 'k--', linewidth=2.5,
                          label=r'numerical $(Re = {0})$'.format(re))
        lines.append(l)
        l, = self.ax.plot(aoa, cl, 'o', markersize=10,
                          label='experimental $c_{l}$')
        lines.append(l)

        self.ax.legend(loc='lower right')

        return lines

def plot_cp_compared(x, cpu, cpl, aoa, re):
    p = ComparedPlot()
    return p.plot(x, cpu, cpl, aoa, re)

class ComparedPlot(object):

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=100)

    def plot(self, x, cpu, cpl, aoa, re='6e+6'):
        lines = []

        # now we compare reference (numerical) data with the experimental ones
        # data taken from Xfoil
        f = os.path.join(os.path.dirname(__file__),
                         'data/naca0018-cpx-aoa{}.txt'.format(aoa))
        numerical_data = np.loadtxt(f, dtype=float).T

        self.ax.set_xlim(0.0, 1.0)
        if aoa == 0:
            self.ax.set_ylim(-4, 1.5)
        else:
            self.ax.set_ylim(np.amin(numerical_data[1]) - 0.4, 1.5)

        self.ax.set_title("$C_{p}$ at $AOA = %d^\circ$"
                          % (aoa))
        self.ax.set_xlabel(r'$x/c$')
        self.ax.set_ylabel('$C_{p}$')

        self.ax.invert_yaxis()

        #self.ax.grid()

        l, = self.ax.plot(x, cpu, color='r', linestyle='-', marker='o',
                          markersize=7, linewidth=1,
                          label='upper')
        lines.append(l)
        l, = self.ax.plot(x, cpl, color='b', linestyle='-', marker='o',
                          markersize=7, linewidth=1,
                          label='lower')
        lines.append(l)

        ii = int(numerical_data.shape[1] / 2)
        l, = self.ax.plot(numerical_data[0, ii::], numerical_data[1, ii:0:-1],
                          color='k', linestyle='-', linewidth=1.5,
                          label=r'numerical $(Re = {0})$'.format(re))
        lines.append(l)
        l, = self.ax.plot(numerical_data[0, ii::], numerical_data[1, ii::],
                          color='k', linestyle='-', linewidth=1.5)
        lines.append(l)
        l, = self.ax.plot(numerical_data[0, ii::], numerical_data[1, ii::]*0+1,
                          color='g', linestyle='--', linewidth=2,
                          label='stagnation point')
        lines.append(l)

        self.ax.legend(loc='upper right')

        return lines
