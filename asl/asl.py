import numpy as np
import itertools

def rms(y):
    N = len(y)
    y = np.array(y)
    y -= np.nanmean(y)
    rms = np.sqrt(np.sum(y**2) / N)
    return rms

def trim_trace(elapset, ts, te, traces):
    ts_idx = np.argmin(np.abs(elapset-ts))
    te_idx = np.argmin(np.abs(elapset-te))+1
    traces_trim = []
    for i in range(traces.shape[0]):
        traces_trim.append(traces[i][ts_idx:te_idx])

    return np.array(traces_trim)

def asl(click_X, click_Y, STX, STY, st_name_list, stream):
    Ns = len(STX)
    print('Ns', Ns)
    Q = 50    
    V = 2000
    low_pass, high_pass = 4, 8
    f = 0.5*(low_pass+high_pass)
    B = (np.pi*f) / (Q*V)
    As = 1.0
    
    Site_amp = {
        'N.ASIV': 1.0,
        'N.ASHV': 1.3704,
        'N.ASNV': 0.915118,
        'N.ASTV': 1.23289,
        'V.ASO2': 1.00309,
        'V.ASOB': 6.83736,
        'V.ASOC': 5.61637
    }

    p_list = list(itertools.permutations(list(range(Ns)), 2))
    Npair = len(p_list)

    model_vals = np.zeros((Npair,2))
    model_vals_plot = np.zeros((Ns,(Ns-1)*2))*np.nan
    model_vals_count = np.zeros(Ns, dtype='int64')
    distance_dict = {}
    for idx in range(Npair):
        i, j = p_list[idx]
        r1 = np.sqrt( (click_X-STX[i])**2 + (click_Y-STY[i])**2 )
        S1 = Site_amp[st_name_list[i]]
        A_model1 = As * S1 * np.exp(-B*r1)/r1**0.5

        r2 = np.sqrt( (click_X-STX[j])**2 + (click_Y-STY[j])**2 )
        S2 = Site_amp[st_name_list[j]]
        A_model2 = As * S2 * np.exp(-B*r2)/r2**0.5

        model_vals[idx,1] = A_model1/A_model2
        
        model_vals[idx,0] = r1
        distance_dict[st_name_list[i]] = r1
        
        idx1 =  st_name_list.index(st_name_list[i])
        idx2 =  st_name_list.index(st_name_list[j])
        model_vals_plot[idx1, model_vals_count[idx1]] =  A_model1/A_model2
        model_vals_count[idx1] += 1
        model_vals_plot[idx2, model_vals_count[idx2]] =  A_model1/A_model2
        model_vals_count[idx2] += 1

    
        
    p_list = list(itertools.permutations(list(range(len(stream))), 2))
    Npair = len(p_list)
    obs_vals = np.zeros((Npair,2))
    obs_vals_plot = np.zeros((len(stream),(len(stream)-1)*2))*np.nan
    obs_vals_count = np.zeros(len(stream), dtype='int64')
    for idx in range(Npair):
        i, j = p_list[idx]

        rms1 = stream[i]
        rms2 = stream[j]
        obs_vals[idx,0] = distance_dict[st_name_list[i]]
        obs_vals[idx,1] = rms1/rms2
        
        idx1 =  st_name_list.index(st_name_list[i])
        idx2 =  st_name_list.index(st_name_list[j])
        obs_vals_plot[idx1, obs_vals_count[idx1]] =  rms1/rms2
        obs_vals_count[idx1] += 1
        obs_vals_plot[idx2, obs_vals_count[idx2]] =  rms1/rms2
        obs_vals_count[idx2] += 1


    SSR = np.sum( (obs_vals[:,1]-model_vals[:,1])**2 ) / Npair

    return SSR


