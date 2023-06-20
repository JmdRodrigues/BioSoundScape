from pyo import *
s = Server().boot()

# Noisy source.
a = PinkNoise(fade)

# These LFOs modulate the `freq`, `spread` and `q` arguments of
# the Phaser object. We give a list of two frequencies in order
# to create two-streams LFOs, therefore a stereo phasing effect.
lf1 = Sine(freq=[0.1, 0.15], mul=100, add=250)
lf2 = Sine(freq=[0.18, 0.13], mul=0.4, add=1.5)
lf3 = Sine(freq=[0.07, 0.09], mul=5, add=6)

# Apply the phasing effect with 20 notches.
b = Phaser(a, freq=lf1, spread=lf2, q=lf3, num=20, mul=0.5).out()

s.gui(locals())