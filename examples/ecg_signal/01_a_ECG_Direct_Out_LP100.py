from pyo import *

s = Server().boot()

path = "../../data/ecg_wav.wav"

# stereo playback without shift in the playback
sf = SfPlayer(path, speed=[1, 1], loop=True, mul=0.4).out()

sf_lp = Tone(sf, freq=100).out()

sf_lp.ctrl()

s.gui()
