import numpy as np
import matplotlib.pyplot as plt
import sys


dem = np.load('../mapdata/dem.npz')
X = dem['x']
Y = dem['y']
Z = dem['z']
STXY = np.load('../mapdata/stxy.npz')
STX = STXY['stx']
STY = STXY['sty']
STX_idx = STXY['stx_idx']
STY_idx = STXY['sty_idx']
Crxy = np.load('../mapdata/craterxy.npz') 
Crx = Crxy['x']
Cry = Crxy['y']

fig = plt.figure(figsize=(6,6))
ax = plt.subplot(111)
im = ax.pcolormesh(X, Y, Z, cmap='terrain', vmin=-400, vmax=1600, rasterized=True)
ax.scatter(STX, STY, marker='v', color='k', s=60)
ax.scatter(X[Crx], Y[Cry], marker='^', color='red', s=60)

stations = ['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC']
for i in range(len(stations)):
    if stations[i]=='V.ASOB':
        ax.annotate(stations[i], # this is the text
            (STX[i],STY[i]), # these are the coordinates to position the label
            textcoords="offset points", # how to position the text
            xytext=(-5,6), # distance from text to points (x,y)
            ha='right', fontsize=14) # horizontal alignment can be left, right or center
    elif stations[i]=='V.ASO2':
        ax.annotate(stations[i], # this is the text
            (STX[i],STY[i]), # these are the coordinates to position the label
            textcoords="offset points", # how to position the text
            xytext=(-2,6), # distance from text to points (x,y)
            ha='left', fontsize=14) # horizontal alignment can be left, right or center
    else:
        ax.annotate(stations[i], # this is the text
            (STX[i],STY[i]), # these are the coordinates to position the label
            textcoords="offset points", # how to position the text
            xytext=(0,8), # distance from text to points (x,y)
            ha='center', fontsize=14) # horizontal alignment can be left, right or center

plt.xlabel('Easting [m]', fontsize=14)
plt.ylabel('Northing [m]', fontsize=14)
plt.tight_layout()

plt.savefig("map.png", dpi=300, bbox_inches="tight", pad_inches=0.05)
plt.show()
