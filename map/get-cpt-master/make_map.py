import numpy as np
    
def load_map(volc, chtbl):
    DEM = np.load('map/mapdata/dem.npz')
    Raster = DEM['z']
    lonm = DEM['x']
    latm = DEM['y']
    STXY = np.load('map/mapdata/stxy.npz')
    STX = STXY['stx']
    STY = STXY['sty']
    STX_idx = STXY['stx_idx']
    STY_idx = STXY['sty_idx']
    Crxy = np.load('map/mapdata/craterxy.npz') 
    Crx = Crxy['x']
    Cry = Crxy['y']

    return Raster, STX, STY, STX_idx, STY_idx, Crx, Cry, lonm, latm 
    
    
    
