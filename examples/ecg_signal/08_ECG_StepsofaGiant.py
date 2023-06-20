from pyo import *

s = Server().boot()

# Large spectrum source.
src = SfPlayer("../../data/ecg_wav.wav")
ex = BrownNoise(.5)
voc = Vocoder(src, ex, freq=20, spread=0.4, q=3.8, slope=0.2, stages=40)
voc.ctrl()
out = voc.mix(2).out()

s.gui(locals())