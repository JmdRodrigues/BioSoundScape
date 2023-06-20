from pyo import *
from plux_device import In_BiosignalsPlux

import numpy as np

class SoundGenerator():
    def __init__(self):
        self.s = Server().boot()
        self.freq_slider = SigTo(value=100, time=0.001, init=100)
        self.amp_slider = SigTo(value=0.3, time=0.025, init=0)

        snd = HarmTable([0.5, 0, 0.33, 0, .2, 0, .143, 0, .111])
        self.scl = EventScale(root="C", scale="major", first=4, octaves=3)
        self.scl_ind = SigTo(value=self.scl[0], time=0.025, init=1)
        # self.e = Events(midinote=self.scl_ind, beat=1, dur=2)
        # self.osc = Sine(freq=self.freq_slider, mul=self.amp_slider)
        self.osc = Sine(freq=440, mul=0.3)
        # self.osc = Sine(freq=midiToHz(self.scl[0]), mul=0.3)

    def start(self):
        self.osc.out(2)
        # self.e.play()
        self.s.start()

    def stop(self):
        self.s.stop()


class BioSound():
    def __init__(self, mac="00:07:80:8C:AD:C9", fs=1000):
        self.mac = mac
        self.fs = fs
        self.n_frames = 128  # size of buffer
        self.n_i = 0  # index in buffer
        self.arr = []
        self.push_buffer = np.zeros((self.n_frames, 1))  # configure buffer

    def setup(self):
        """
        Configures the NewDevice from BiosignalsPlux
        Configures the Pyo Sound Class
        :return:
        """
        self.sound = SoundGenerator()
        self.device = In_BiosignalsPlux(self.mac, freq=self.fs)  # biosignals device

    def start(self):
        # start pyo
        self.sound.start()
        # start bioplux
        self.device._set_on_data(self.store_in_buffer)
        self.device._onstart()

    def stop(self):
        if self.device is None:
            print('Nothing to stop')
        else:
            self.device._onstop()

        if self.sound is None:
            print("No sound to stop")
        else:
            self.sound.stop()

    def amp_val(self, val):
        return val

    def store_in_buffer(self, nseq, fn):
        # self.sound.freq_slider.value = 250
        # print(float(abs(self.device.transferFunction(fn))[0])/3.6)
        # self.sound.amp_slider.value = float(abs(self.device.transferFunction(fn))[0]/3.6)
        # print(t_in-self.device.t0)
        # print(nseq, t_in - self.device.t0)
        # self.arr.append(t_in - self.device.t0)

        # print(self.device.transferFunction(fn[0]))

        if (self.n_i < self.n_frames):
            self.push_buffer[self.n_i, :] = self.device.transferFunction(fn[0])
            # self.push_buffer[self.n_i, :] = fn[0]-32768
            self.n_i += 1
        else:
            self.push_buffer[0:-1, :] = self.push_buffer[1:, :]
            self.push_buffer[-1, :] = self.device.transferFunction(fn[0])
            # self.push_buffer[-1, :] = fn[0]-32768
            self.n_i += 1

        # Experience 1

        # Experience 2

        # Experience 3

        # Experience 4

        # if(nseq%500==0):
        # amp_ = len(self.sound.scl) * np.mean(np.abs(self.push_buffer))
        # print(self.sound.scl[int(amp_)])
        # self.sound.scl_ind.value = self.sound.scl[int(amp_)]
        amp = abs(self.device.transferFunction(fn[0])) / 1.5
        # amp = 1000*float(np.mean(abs(self.push_buffer)))
        # print(amp)
        # self.sound.osc.setFreq(100+float(500*amp))

        # self.sound.scl_ind = self.sound.scl[2*int(amp_)]
        # print(self.sound.scl[2*int(amp_)])
        # amp_ = 250*np.abs(self.device.transferFunction(fn[0]))/3.6
        # self.sound.osc.setFreq(midiToHz(self.sound.scl[int(amp_)]))
        # self.sound.osc.setFreq(440 + int(amp**1.5))

        # self.sound.osc.setMul(250 + int(5*amp_))
        # self.sound.freq_slider.value =


if __name__ == "__main__":
    session = BioSoundScape()
    session.setup()
    session.start()
    session.stop()
