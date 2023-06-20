"""
03-read-from-ram.py - Soundfile playback from RAM.

Reading a sound file from the RAM gives the advantage of a very
fast access to every loaded samples. This is very useful for a
lot of processes, such as granulation, looping, creating envelopes
and waveforms and many others.

The simplest way of loading a sound in RAM is to use the SndTable
object. This example loads a sound file and reads it in loop.
We will see some more evolved processes later...

"""
from pyo import *

s = Server().boot()

path = "../../data/ecg_wav.wav"

sf = SfPlayer(path)

# Use an envelope follower to track the amplitude of the input
follower = Follower(sf, 10)

# simple pulsar waveform
t = HarmTable([1, 0, 0.3, 0, 0.2, 0, 0, 0.1], size=32768)

# Use the follower to modulate the amplitude of a Sine wave
osc = Osc(table=t, freq=220, mul=follower).out()

s.gui(locals())
