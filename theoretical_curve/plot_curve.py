import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
import matplotlib.dates as mdates


plt.style.use(['science','nature'])
plt.rcParams['mathtext.fontset'] = 'stix' # math fontの設定
plt.rcParams["axes.facecolor"] = (1,1,1,0)
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.direction'] = "out"
plt.rcParams['ytick.direction'] = "out"
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['axes.edgecolor'] = '#08192D'
plt.rcParams['axes.labelcolor'] = '#08192D'
plt.rcParams['xtick.color'] = '#08192D'
plt.rcParams['ytick.color'] = '#08192D'
plt.rcParams['text.color'] = '#08192D'
plt.rcParams['legend.framealpha'] = 1.0
plt.rcParams['xtick.major.pad']='8'



fc = 6.0 
R = np.linspace(0.01,10000,1000)
A0 = 1
S = 1

fig = plt.figure(figsize=(6,6))

ax1 = plt.subplot(111)
Q = [10, 50, 100]
V = 2000.0
for cc, Q_val in enumerate(Q):
    B = (np.pi*fc)/(Q_val*V)
    A = (1/np.sqrt(R)) * np.exp(-B*R)
    ax1.plot(R,A, label='V=2000 [m/s], Q='+str(Q_val), lw=2, color='C'+str(cc))

V = 500.0
for cc, Q_val in enumerate(Q):
    B = (np.pi*fc)/(Q_val*V)
    A = (1/np.sqrt(R)) * np.exp(-B*R)
    ax1.plot(R,A, label='V=500 [m/s], Q='+str(Q_val), lw=2, ls='--', color='C'+str(cc))

ax1.set_xlim(500,6000)
ax1.set_ylim(0,0.04)
ax1.legend(fontsize=14)
ax1.set_xlabel(r'$r$ [m]', fontsize=14)
ax1.set_ylabel('amplitude', fontsize=14)


plt.savefig('curve.png', dpi=300, transparent=False)
plt.show()