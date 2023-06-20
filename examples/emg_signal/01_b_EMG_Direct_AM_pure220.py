from pyo import *

s = Server().boot()

path = "../../data/emg_env.wav"

sf = SfPlayer(path)

# Use an envelope follower to track the amplitude of the input
follower = Follower(sf, 100)

# Use the follower to modulate the amplitude of a Sine wave
sine = Sine(freq=220, mul=follower)

# Output the modulated Sine wave
sine.out()

s.gui(locals())