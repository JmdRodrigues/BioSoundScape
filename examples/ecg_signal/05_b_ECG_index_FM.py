from pyo import *
import random

path = "../../data/ecg_wav.wav"
s = Server().boot()

sf = SfPlayer(path)

car = [random.triangular(150, 155) for i in range(10)]
rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(10)]
ind = [random.randint(2, 6) for i in range(10)]

fm = FM(carrier=car, ratio=1, index=sf*2, mul=.05).out()

s.gui(locals())