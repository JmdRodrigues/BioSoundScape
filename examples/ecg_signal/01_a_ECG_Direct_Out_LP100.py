from pyo import *

s = Server().boot()

path = "../../data/ecg_wav.wav"

# stereo playback without shift in the playback
sf = SfPlayer(path, speed=[1, 1], loop=True, mul=0.4)
sf_lp = Tone(sf, freq=25)
sf_log = Log10(1+sf_lp).out()

sf_lp.ctrl()

s.gui()
