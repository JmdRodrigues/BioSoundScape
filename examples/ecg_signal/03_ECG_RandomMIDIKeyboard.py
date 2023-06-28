from pyo import *

"""
Random keyboard generator in synch with the detection of a beat in the ECG signal
"""

path = "../../data/ecg_wav.wav"

s = Server().boot()

sf_player = SfPlayer(path, speed=[1, 1])

b = Thresh(sf_player, threshold=[0.5], dir=0)
env = CosTable([(0, 0), (100, 1), (1024, 0.5), (7000, 0.5), (8192, 0)])
amp = TrigEnv(b, table=env, dur=1, mul=.3)
# Generates a midi note for each trigger from Beat in a pseudo-random distribution
# print([i for i in EventScale(root="E", scale="majorPenta", first=4, octaves=2, type=0)])
scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
freq = TrigChoice(b, scl)
sine = Sine(freq=[freq, freq], mul=amp*.5).out()

s.gui(locals())