from pyo import *

s = Server().boot()

path = "../../data/emg_env.wav"
song = "../../data/music/onclassical_demo_fiati-di-parma_thuille_terzo-tempo_sestetto_small-version.wav"

# stereo playback without shift in the playback
sf = SfPlayer(path, speed=[1, 1], loop=True, mul=0.4)
musicf = SfPlayer(song, speed = [1+sf, 1+sf], mul=.3).out()

s.gui()