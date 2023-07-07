import numpy as np

def scale(sig, max_):
    """
    Scale the signal in relation to the maximum measured
    EMG_max: 0.3
    ECG_max: ...
    ACC_max: ...
    """
    return sig/max_

def scale_mul(sig):
    return 0.5*sig

def scale_freq(sig, octave=5):
    freq_factor = 440*(2**octave)
    return freq_factor*sig

def scale_index(sig):
    return 3*sig

def scale_voice(sig, nbr_waves):
    return nbr_waves*sig

def scale_key_selector(sig, nbr_keys):
    return nbr_keys*sig

def tf_tanh_audio(sig, max_):
    return np.tanh(3*scale(sig, max_))

def tf_lin_audio(sig, max_):
    return scale(sig, max_)

def tf_arctanh_audio(sig, max_):
    return np.arctanh(0.8*scale(sig, max_))**2