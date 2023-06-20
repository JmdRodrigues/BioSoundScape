from pyo import *

s = Server().boot()

path = "../../data/emg_raw.wav"

# stereo playback without shift in the playback
sf = SfPlayer(path, speed=[1, 1], loop=True, mul=0.2).out()

s.gui()
