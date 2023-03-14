import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
import pandas as pd
import os

cptpath = r'../map/get-cpt-master'
sys.path.append(cptpath)
import make_map

cptpath = r'../asl'
sys.path.append(cptpath)
import asl


# if st.button(label='show results'):
try:
    X = np.array(st.session_state['asl'])[:,0]
    Y = np.array(st.session_state['asl'])[:,1]
    SSRS = np.array(st.session_state['asl'])[:,2] 
    SSRS /= np.min(SSRS)
    station_list = st.session_state['ustations']
    Ns = len(station_list)

    raster, STX0, STY0, STX_idx0, STY_idx0, Crx, Cry, lonm, latm = make_map.load_map('Aso', 'map/get-cpt-master/Aso.ch') 
    STX = []; STY = []
    STX_idx = []; STY_idx = []
    for i in range(len(station_list)):
        STX.append(STX0[['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC'].index(station_list[i])])
        STY.append(STY0[['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC'].index(station_list[i])])
        STX_idx.append(STX_idx0[['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC'].index(station_list[i])])
        STY_idx.append(STY_idx0[['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC'].index(station_list[i])])


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
        name="SSR/SSR_min",
        marker=dict(
            size=16,
            color=SSRS,
            colorscale='Viridis_r',
            showscale=True,
            cmin = 1,
            cmax = 1.3,
        ),
        
        
    ) 
    plot.append(ssr_scatt)

    for i in range(Ns):
        station_locs = go.Scatter(x=[STX_idx[i]], y=[STY_idx[i]], hoverinfo='skip', mode='markers+text', textposition="top center",  marker_symbol='triangle-down',  text=[station_list[i]], marker=dict(color='black', size=10))
        plot.append(station_locs)


    fig = go.Figure(data =
        plot,
    )
    fig.update_layout(width=600, height=600)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, theme=None)

except:
    st.markdown("Did you forget to save ASL result?")