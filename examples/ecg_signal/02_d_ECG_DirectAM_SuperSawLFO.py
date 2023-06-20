from pyo import *

"""
Random keyboard generator in synch with the detection of a beat in the ECG signal
"""
s = Server().boot()
src = SfPlayer("../../data/ecg_wav.wav")
# Roland JP-8000 Supersaw emulator.
lfo4 = Sine(0.1).range(0.1, 0.75)
osc4 = SuperSaw(freq=440, detune=lfo4, mul=[0.05, 0.25*src]).out()

s.gui(locals())