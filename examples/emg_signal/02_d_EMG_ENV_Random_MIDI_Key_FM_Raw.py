
from pyo import *

"""
Random keyboard generator in synch with the detection of a beat in the ECG signal
"""

path = "../../data/emg_env.wav"

#
s = Server().boot()
#
sf_player = SfPlayer(path, speed=[1, 1])
sf_player2 = SfPlayer(path, speed=[1, 1])

b = Thresh(sf_player, threshold=[0.1, 0.5, 0.8], dir=2)
env = CosTable([(0, 0.5), (100, 0.5), (1024, 0.5), (7000, 0.5), (8192, 0.5)])
amp = TrigEnv(b, table=env, dur=1.5, mul=.3)

# Generates a midi note for each trigger from Beat in a pseudo-random distribution
scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
freq = TrigChoice(b, scl)
sine = Sine(freq=[freq, freq], mul=amp*.5).out()
sine2 = Sine(freq=[freq, freq], mul=amp*.5).out(1)

g_sharp_freq = 277.183
delta_ = 2
nbr_waves = 50
car = [random.triangular(g_sharp_freq-delta_, g_sharp_freq+delta_) for i in range(nbr_waves)]
rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
fm = FM(carrier=car, ratio=rat, index=sf_player2, mul=1.5/nbr_waves).out()

s.gui(locals())
