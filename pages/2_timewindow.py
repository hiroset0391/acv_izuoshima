import streamlit as st
from streamlit_plotly_events import plotly_events
import numpy as np
import plotly.graph_objects as go
from plotly import subplots
import os, sys
import pandas as pd
import scipy.signal as ssig
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

def cosTaper(windL, percent):
    N = windL
    tp = np.ones(N)
    for i in range(int(N * percent + 1)):
        tp[i] *= 0.5 * (1 - np.cos((np.pi * i) / (N * percent)))

    for i in range(int(N * (1 - percent)), N):
        tp[i] *= 0.5 * (1 - np.cos((np.pi * (i + 1)) / (N * percent)))

    return tp


@st.cache_data(persist="disk")
def make_rms_list():
    lst = []
    return lst


#colors = ['#F75C2F', '#2EA9DF', '#7BA23F', 'blue', 'green', 'orange', 'red']
#station_list = ['N.ASIV', 'N.ASHV', 'N.ASNV', 'N.ASTV',  'V.ASOB', 'V.ASO2', 'V.ASOC']

station_list = st.session_state['ustations']


st.header('define frequency band')

with st.expander('See spectrogram'):
    image = Image.open('spectrogram/spec_V.ASO2.png')
    st.image(image, width=680)


Fs = 20.0
nyq = 0.5 * Fs
fmin, fmax = st.slider(label='',
            min_value=0.01,
            max_value=9.99,
            value=(4.0, 8.0),
            )

[b12, a12] = ssig.butter(3, Wn=[fmin/nyq, fmax/nyq], btype='bandpass')


Trs = []
for station in station_list:
    data = np.load('data/tr_'+station+'.npz')
    elapset = data['t']
    tr = data['y']
    tp = cosTaper(len(tr), 0.01)
    tr *= tp
    tr = ssig.filtfilt(b12, a12, tr)
    tr -= np.nanmean(tr)
    Trs.append(tr)
Trs = np.array(Trs)
maxamp = np.nanmax( np.nanmax(Trs, axis=1) )
Trs /= maxamp

Ns = len(Trs)




st.header('define time window')
if 'ts' not in st.session_state: 
    st.session_state.ts = np.nan #countがsession_stateに追加されていない場合，0で初期化

if 'te' not in st.session_state: 
    st.session_state.te = np.nan #countがsession_stateに追加されていない場合，0で初期化

time_window = st.radio('', ("define starttime", "define endtime"), horizontal=True)

fig = subplots.make_subplots(rows=Ns, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles=station_list)

for i in range(Ns):
    fig.update_yaxes(title="amp.", row=i+1, col=1) # Y軸タイトルを指定

    fig.update_xaxes(range=(elapset[0], elapset[-1]), row=i+1, col=1) # Y軸の最大最小値を指定
    
    trace0 = go.Scatter(x=elapset, y=Trs[i], name=station_list[i], mode="lines", showlegend=False, line=dict(color='black'))
    fig.append_trace(trace0, i+1, 1)

fig.update_xaxes(title="time [s]", row=Ns, col=1)
fig.update_layout(width=700, height=1000) #

selected_points = plotly_events(fig, click_event=True)

if len(selected_points)>0:
    selected_points = selected_points[0]
    x_start = selected_points["x"]
    x_start_idx = selected_points["pointIndex"]
    if time_window=='define starttime':
        
        st.session_state.ts = x_start
    if time_window=='define endtime':
        st.session_state.te = x_start

    

st.markdown("#### starttime="+str(st.session_state.ts)+"   endtime="+str(st.session_state.te))


if st.button(label='save rms amplitude'):

    Trs_trim = asl.trim_trace(elapset, st.session_state.ts, st.session_state.te, Trs)
    rms_vals = []
    for i in range(Ns):
        rms_vals.append(rms(Trs_trim[i]))

    rms_list = make_rms_list()
    for i in rms_vals:
        rms_list.append(i)

    st.session_state['rms'] = rms_list

    st.write('saved')
    df_rms = pd.DataFrame({'station': station_list, 'RMS': st.session_state['rms']})
    st.dataframe(df_rms)
