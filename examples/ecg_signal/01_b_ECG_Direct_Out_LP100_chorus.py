from pyo import *

path = "../../data/ecg_wav.wav"

s = Server().boot()
a = SfPlayer(path=path,
             speed=[1,1.005,1.007,.992], loop=True, mul=.25)

sf_lp = Tone(a, freq=100).out()

s.gui(locals())