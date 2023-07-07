import numpy as np
import matplotlib.pyplot as plt

import time

from pyo import *

import math

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

def scale_freq(sig, octave=3):
    freq_factor = 440*(2**octave)
    return freq_factor*sig

def scale_voice(sig, nbr_waves):
    return nbr_waves*sig

def tf_tanh_emg_audio(sig):
    return np.tanh(3*scale(sig))

def tf_lin_emg_audio(sig):
    return scale(sig)

def tf_arctanh_emg_audio(sig):
    return np.arctanh(0.8*scale(sig))**2

aud_lim = [0.0, 0.5]
max_sig = np.loadtxt("max_vals.txt")[:, 1]

aud_sig = np.linspace(aud_lim[0], aud_lim[1], 1000)
sig = np.linspace(0, min(max_sig), 1000)

s = Server().boot()
s.start()

# sel = Selector([Sine(freq=(2**i)*440, mul=0.3) for i in range(0, 3)]).out()
sine = Sine(freq=440, mul=0.3).out()
# out_ = scale_voice(tf_emg_audio(sig), 3)
# out_ = scale_voice(tf_tanh_emg_audio(sig), 3)
out_mul = scale_freq(tf_tanh_emg_audio(sig))

plt.plot(out_mul)
plt.show()
i = 0

while True:
    # sel.setVoice(float(out_[i]))
    sine.setFreq(float(out_mul[i]))
    time.sleep(0.01)
    i+=1
    # print(float(out_[i]))




# sig = np.min(max_sig)*np.random.random(1000)

# audio_out = f(sig)


# plt.plot(np.tanh(2*scale(sig)))
# plt.show()