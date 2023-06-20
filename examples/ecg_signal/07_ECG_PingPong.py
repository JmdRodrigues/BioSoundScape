from pyo import *

s = Server(duplex=0).boot()

# soundfile = SndTable(SNDS_PATH + "/transparent.aif")
soundfile = SndTable("../../data/ecg_wav.wav")

src = Looper(soundfile, dur=2, xfade=0, mul=0.3)
src2 = src.mix(2).out()

# Four parallel stereo comb filters. The delay times are chosen
# to be as uncorrelated as possible. Prime numbers are a good
# choice for delay lengths in samples.
comb1 = Delay(src, delay=[0.0297, 0.0277], feedback=0.65)
comb2 = Delay(src, delay=[0.0371, 0.0393], feedback=0.51)
comb3 = Delay(src, delay=[0.0411, 0.0409], feedback=0.5)
comb4 = Delay(src, delay=[0.0137, 0.0155], feedback=0.73)

combsum = src + comb1 + comb2 + comb3 + comb4
# combsum = src + comb1

# The sum of the original signal and the comb filters
# feeds two serial allpass filters.
all1 = Allpass(combsum, delay=[0.005, 0.00507], feedback=0.75)
all2 = Allpass(all1, delay=[0.0117, 0.0123], feedback=0.61)

# Brightness control.
lowp = Tone(all2, freq=3500, mul=0.25).out()

s.gui(locals())