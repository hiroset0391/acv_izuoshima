import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
import pandas as pd

cptpath = r'../map/get-cpt-master'
sys.path.append(cptpath)
import make_map

cptpath = r'../asl'
sys.path.append(cptpath)
import asl


# if st.button(label='show results'):
    
df_in = pd.read_csv('tmpfiles/asl_results.csv')
X = np.array(df_in['X'])
Y = np.array(df_in['Y'])
SSRS = np.array(df_in['SSR'])

raster, STX, STY, STX_idx, STY_idx, Crx, Cry, lonm, latm = make_map.load_map('Aso', 'map/get-cpt-master/Aso.ch') 
plot = []
basemap = go.Contour(
        z=raster,
        zmin=0,
        zmax=1600,
        colorscale='Earth_r',
        name="Elevation [m]",
        showscale=False,
        hoverinfo='skip',
        contours=dict(
            start=0,
            end=1600,
            size=150,
        ),
        
)

plot.append(basemap)

# basemap = go.Surface(z=raster, x=lonm, y=latm, colorscale='Earth_r')
# plot.append(basemap)

# basemap = go.Surface(z=np.zeros((raster.shape[0], raster.shape[1])), x=lonm, y=latm, colorscale='Earth_r')
# plot.append(basemap)

# basemap = go.Surface(z=-np.ones((raster.shape[0], raster.shape[1]))*1000, x=lonm, y=latm, colorscale='Earth_r')
# plot.append(basemap)

crater_loc = go.Scatter(x=Crx, y=Cry, mode='markers', hoverinfo='skip', marker_symbol='triangle-up', marker=dict(color='red', size=15))
plot.append(crater_loc)

ssr_scatt = go.Scatter(
    x=X,
    y=Y,
    mode='markers',
    name="SSR",
    marker=dict(
        size=16,
        color=SSRS,  # マーカーの色をyにする
        colorscale='Viridis_r',  # カラースケール変更
        showscale=True  # カラーバーの表示
    ),
    
) 
plot.append(ssr_scatt)

fig = go.Figure(data =
    plot,
)
fig.update_layout(width=600, height=600)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, theme=None)

    