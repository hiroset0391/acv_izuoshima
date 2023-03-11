import streamlit as st
from streamlit_plotly_events import plotly_events
import numpy as np
import plotly.graph_objects as go
import sys
import pandas as pd
import os

cptpath = r'map/get-cpt-master'
sys.path.append(cptpath)
import make_map

cptpath = r'../asl'
sys.path.append(cptpath)
import asl


# df_in = pd.read_csv('tmpfiles/rms.csv')
# station_list = list(df_in['station'])
# Ns = len(station_list)
# rms_vals = np.array(df_in['rms'])
rms_vals = np.array( st.session_state['rms'] )
Ns = len(rms_vals)
station_list = st.session_state['ustations']

# @st.cache_resource()
# def cache_lst():
#     lst = []
#     return lst

@st.cache_data(persist="disk")
def cache_lst():
    lst = []
    return lst

@st.cache_data(persist="disk")
def make_asl_list():
    lst = []
    return lst

#@st.cache_data
def get_chart_77100278(stream, ustations, ssr_vals):
    #raster, STX, STY, Crx, Cry = make_map.show_map('Aso', '../map/get-cpt-master/Aso.ch', station_list)
    raster, STX0, STY0, STX_idx0, STY_idx0, _, _, lonm, latm = make_map.load_map('Aso', 'map/get-cpt-master/Aso.ch') 

    STX = []; STY = []
    STX_idx = []; STY_idx = []
    for i in range(len(ustations)):
        STX.append(STX0[['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC'].index(ustations[i])])
        STY.append(STY0[['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC'].index(ustations[i])])
        STX_idx.append(STX_idx0[['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC'].index(ustations[i])])
        STY_idx.append(STY_idx0[['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC'].index(ustations[i])])
    
    
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
    # print(raster.shape)
    # Ny, Nx = raster.shape
    # Ny_decim = Ny//10
    # Nx_decim = Nx//10
    # basemap = go.Surface(z=np.zeros((Ny_decim, Nx_decim)), x=lonm[::10], y=latm[::10], colorscale='Earth_r', showscale=False)
    # plot.append(basemap)

    # basemap = go.Surface(z=-np.ones((raster.shape[0], raster.shape[1]))*1000, x=lonm, y=latm, colorscale='Earth_r')
    # plot.append(basemap)

    
    for i in range(Ns):
        station_locs = go.Scatter(x=[STX_idx[i]], y=[STY_idx[i]], hoverinfo='skip', mode='markers+text', textposition="top center",  marker_symbol='triangle-down',  text=[station_list[i]], marker=dict(color='black', size=10))
        plot.append(station_locs)

    # crater_loc = go.Scatter(x=Crx, y=Cry, mode='markers', hoverinfo='skip', marker_symbol='triangle-up', marker=dict(color='red', size=15))
    # plot.append(crater_loc)



    fig = go.Figure(data =
        plot
        )
    fig.update_layout(width=600, height=600) # 図の高さを幅を指定
    fig.update_layout(showlegend=False)

    
    selected_points = plotly_events(fig, click_event=True)
    source_x = np.nan
    source_y = np.nan
    #SSRs = cache_lst()
    if len(selected_points)>0:
        selected_points = selected_points[0]
        source_x_idx = selected_points['x']
        source_y_idx = selected_points['y']
        source_x = lonm[source_x_idx]
        source_y = latm[source_y_idx]
        
        SSR = asl.asl(source_x, source_y, STX, STY, ustations, stream)
        ssr_vals.append([SSR, source_x_idx, source_y_idx])

        try:
            ssr_arr = st.session_state['ssr']
            print(ssr_arr)
            ssr_arr.append([SSR, source_x_idx, source_y_idx])
            st.session_state['ssr'] = ssr_arr
        except:
            st.session_state['ssr'] = [[SSR, source_x_idx, source_y_idx]]
    
    
    return ssr_vals


ssr_vals = cache_lst()
SSRs = get_chart_77100278(rms_vals, station_list, ssr_vals)


col1, col2, _, _ = st.columns(4)

with col1:
    if st.button(label='clear'):
        #st.cache_resource.clear()
        del st.session_state['ssr']

        try:
            SSRs.clear()
            del st.session_state['asl']
        except:
            pass

try:
    if len(st.session_state['ssr'])>0: 
        #df_gridsearch = pd.DataFrame({'SSR': np.array(SSRs)[:,0], 'X': np.array(SSRs)[:,1], 'Y': np.array(SSRs)[:,2] })
        df_gridsearch = pd.DataFrame({'SSR': np.array(st.session_state['ssr'])[:,0], 'X': np.array(st.session_state['ssr'])[:,1], 'Y': np.array(st.session_state['ssr'])[:,2] })
        st.table(df_gridsearch)
except:
    st.markdown("Did you forget to conduct ASL?")


with col2:
    if st.button(label='save results'):
        #df = pd.DataFrame({'X': np.array(SSRs)[:,1], 'Y': np.array(SSRs)[:,2], 'SSR': np.array(SSRs)[:,0]})
        #df.to_csv('tmpfiles/asl_results.csv')
        asl_list = make_asl_list()
        for i in range(len(st.session_state['ssr'])):
            asl_list.append([st.session_state['ssr'][i][1], st.session_state['ssr'][i][2], st.session_state['ssr'][i][0]])

        st.session_state['asl'] = asl_list
        st.write('saved')
        