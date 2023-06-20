from pyo import *

s = Server().boot()

path = "../../data/ecg_wav.wav"
sf = SfPlayer(path)

fm = FM(carrier=440, ratio=sf, mul=.1).mix(2).out()

s.gui(locals())