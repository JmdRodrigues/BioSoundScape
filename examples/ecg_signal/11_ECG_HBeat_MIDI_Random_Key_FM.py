from pyo import *

"""
Random keyboard generator in synch with the detection of a beat in the ECG signal
"""

path = "../../data/ecg_wav.wav"

s = Server().boot()

sf_player = SfPlayer(path, speed=[1, 1])
s.start()
b = Thresh(sf_player, threshold=[0.5], dir=0)
env = LinTable([(0,0), (190,.8), (1000,.5), (4300,.1), (8191,0)], size=8192)
amp = TrigEnv(b, table=env, dur=1, mul=.3)
# Generates a midi note for each trigger from Beat in a pseudo-random distribution
scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
freq = TrigChoice(b, scl)
sine = Sine(freq=[freq, freq], mul=amp*.1).out()

g_sharp_freq = 277.183
car = [random.triangular(g_sharp_freq-2, g_sharp_freq+2) for i in range(10)]
rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(10)]
ind = [random.randint(2, 6) for i in range(10)]
fm = FM(carrier=car, ratio=rat, index=sf_player, mul=.05).out()

s.gui(locals())