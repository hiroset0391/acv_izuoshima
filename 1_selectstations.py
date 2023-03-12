import streamlit as st
from streamlit_plotly_events import plotly_events
import numpy as np
import plotly.graph_objects as go
from plotly import subplots
import os, sys
import pandas as pd
import os
from PIL import Image

cptpath = os.getcwd()+r'/asl'
sys.path.append(cptpath)
import asl

def rms(y):
    N = len(y)
    y = np.array(y)
    y -= np.nanmean(y)
    rms = np.sqrt(np.sum(y**2) / N)
    return rms


@st.cache_data(persist="disk")
def make_ustation_list():
    lst = []
    return lst

colors = ['#F75C2F', '#2EA9DF', '#7BA23F', 'blue', 'green', 'orange', 'red']

station_list = ['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC']

st.header('select stations')
image = Image.open('map/img/map.png')
st.image(image, width=400)

col = st.columns(4)
ASIV = col[0].checkbox(label=station_list[0])
ASHV = col[1].checkbox(label=station_list[1])
ASNV = col[2].checkbox(label=station_list[2])
ASTV = col[3].checkbox(label=station_list[3])

col = st.columns(4)
ASOB = col[0].checkbox(label=station_list[4])
ASO2 = col[1].checkbox(label=station_list[5])
ASOC = col[2].checkbox(label=station_list[6])

used_station_list = []; used_station_list_idx = []
if ASIV:
    used_station_list.append(station_list[0])
    used_station_list_idx.append(0)
if ASHV:
    used_station_list.append(station_list[1])
    used_station_list_idx.append(1)
if ASNV:
    used_station_list.append(station_list[2])
    used_station_list_idx.append(2)
if ASTV:
    used_station_list.append(station_list[3])
    used_station_list_idx.append(3)
if ASOB:
    used_station_list.append(station_list[4])
    used_station_list_idx.append(4)
if ASO2:
    used_station_list.append(station_list[5])
    used_station_list_idx.append(5)
if ASOC:
    used_station_list.append(station_list[6])
    used_station_list_idx.append(6)

if st.button(label='save stations'):
    
    ustation_list = make_ustation_list()
    for i in used_station_list:
        ustation_list.append(i)

    st.session_state['ustations'] = ustation_list

    st.write('saved')
    #st.write(ustation_list)