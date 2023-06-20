
from pyo import *

"""
Random keyboard generator in synch with the detection of a beat in the ECG signal
"""

path = "../../data/emg_raw.wav"

s = Server().boot()

sf_player = SfPlayer(path, speed=[1, 1])

b = Thresh(sf_player, threshold=[0.5], dir=2)
env = CosTable([(0, 0.5), (100, 0.5), (1024, 0.5), (7000, 0.5), (8192, 0.5)])
amp = TrigEnv(b, table=env, dur=0.75, mul=.3)

# Generates a midi note for each trigger from Beat in a pseudo-random distribution
scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
freq = TrigChoice(b, scl)
sine = Sine(freq=[freq, freq], mul=amp*.5).out()
sine2 = Sine(freq=[freq, freq], mul=amp*.5).out(1)

s.gui(locals())