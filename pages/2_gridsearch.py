import streamlit as st
from streamlit_plotly_events import plotly_events
import numpy as np
import plotly.graph_objects as go
import sys
import pandas as pd


cptpath = r'map/get-cpt-master'
sys.path.append(cptpath)
import make_map

cptpath = r'../asl'
sys.path.append(cptpath)
import asl


df_in = pd.read_csv('tmpfiles/rms.csv')
station_list = list(df_in['station'])
Ns = len(station_list)
rms_vals = np.array(df_in['rms'])

@st.cache_resource()
def cache_lst():
    lst = []
    return lst

#@st.cache_data
def get_chart_77100278(stream):
    #raster, STX, STY, Crx, Cry = make_map.show_map('Aso', '../map/get-cpt-master/Aso.ch', station_list)
    raster, STX, STY, STX_idx, STY_idx, Crx, Cry, lonm, latm = make_map.load_map('Aso', 'map/get-cpt-master/Aso.ch') 
    
    plot = []
    basemap = go.Contour(
            z=raster,
            zmin=0,
            zmax=1600,
            colorscale='Earth_r',
            name="Elevation [m]",
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


    xshift = [0] * Ns #Position of the annotation (you can also create this for yshift) 
    showarrow = [False] * Ns #No arrow
    font_size = [12] * Ns #Annotation Fontsize


    
    for i in range(Ns):
        station_locs = go.Scatter(x=[STX_idx[i]], y=[STY_idx[i]], hoverinfo='skip', mode='markers+text', textposition="top center",  marker_symbol='triangle-down',  text=[station_list[i]], marker=dict(color='black', size=10))
        plot.append(station_locs)

    crater_loc = go.Scatter(x=Crx, y=Cry, mode='markers', hoverinfo='skip', marker_symbol='triangle-up', marker=dict(color='red', size=15))
    plot.append(crater_loc)



    fig = go.Figure(data =
        plot
        )
    fig.update_layout(width=600, height=600) # 図の高さを幅を指定
    fig.update_layout(showlegend=False)

    
    selected_points = plotly_events(fig, click_event=True)
    source_x = np.nan
    source_y = np.nan
    SSRs = cache_lst()
    if len(selected_points)>0:
        selected_points = selected_points[0]
        source_x_idx = selected_points['x']
        source_y_idx = selected_points['y']
        source_x = lonm[source_x_idx]
        source_y = latm[source_y_idx]
        
        SSR = asl.asl(source_x, source_y, STX, STY, station_list, stream)
        SSRs.append([SSR, source_x_idx, source_y_idx])

    
    
    
    return SSRs


SSRs = get_chart_77100278(rms_vals)

col1, col2, _, _ = st.columns(4)

with col1:
    if st.button(label='clear'):
        st.cache_resource.clear()
        try:
            SSRs.clear()
        except:
            pass

if len(SSRs)>0: 
    df_gridsearch = pd.DataFrame({'SSR': np.array(SSRs)[:,0], 'X': np.array(SSRs)[:,1], 'Y': np.array(SSRs)[:,2] })
    st.table(df_gridsearch)


with col2:
    if st.button(label='save results'):
        df = pd.DataFrame({'X': np.array(SSRs)[:,1], 'Y': np.array(SSRs)[:,2], 'SSR': np.array(SSRs)[:,0]})
        df.to_csv('tmpfiles/asl_results.csv')