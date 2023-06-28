from pyo import *
from tools.plux_device import In_BiosignalsPlux

import numpy as np

def noop():
    pass

class SoundGenerator():
    def __init__(self, example="example0", plot_duration=3, update_spectrum_interval=0.05, on_data=noop):
        self.s = Server().boot()
        self.duration = plot_duration  # Recording duration in seconds
        # sample_rate = 44100  # Sample rate (adjust if necessary)
        # self.frame_update = update_spectrum_interval
        self.frame_update = 0.1
        # Initialize the recording buffer
        self.num_frames = int(self.duration//self.frame_update)
        # self.spec_buffer = np.zeros((self.num_frames, 512))
        # self.x_spec_buffer = np.zeros(self.num_frames)
        # self.freq_buffer = np.zeros(512)
        self.frame_cnt = 0
        # self.x_index = x_index

        self.on_data = on_data

        if(example=="example0"):
            self.example0_init()
        elif(example == "example1"):
            self.example1_init_()
        elif (example == "example2"):
            self.example2_init_()
        elif (example == "example3"):
            self.example3_init_()
        elif (example == "example5"):
            self.example5_init_()

    def example0_init(self):
        self.freq_slider = SigTo(value=100, time=0.001, init=100)
        self.amp_slider = SigTo(value=0.3, time=0.025, init=0)

        snd = HarmTable([0.5, 0, 0.33, 0, .2, 0, .143, 0, .111])
        self.scl = EventScale(root="C", scale="major", first=4, octaves=3)
        self.scl_ind = SigTo(value=self.scl[0], time=0.025, init=1)
        # self.e = Events(midinote=self.scl_ind, beat=1, dur=2)
        # self.osc = Sine(freq=self.freq_slider, mul=self.amp_slider)
        self.osc = Sine(freq=440, mul=0.3)
        self.reader = Spectrum(self.osc, function=self.on_data)
        #spectrum data retrived every 10 ms
        self.reader.polltime(self.frame_update)
        # self.osc = Sine(freq=midiToHz(self.scl[0]), mul=0.3)
    def example1_init_(self):
        # self.b = Thresh(SigTo(0), threshold=[0.025], dir=2)
        # self.env = CosTable([(0, 0), (100, 0.5), (1024, 0.5), (7000, 0.5), (8192, 0)])
        self.env = TriangleTable(order=10)
        # self.amp = TrigEnv(self.b, table=self.env, dur=0.5, mul=.7)
        self.amp = 0
        self.scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
        self.freq = TrigChoice(self.b, self.scl)

        self.sine = Sine(freq=[self.freq, self.freq], mul=self.amp * .2)
        self.sine2 = Sine(freq=[self.freq, self.freq], mul=self.amp * .2)
        g_sharp_freq = 277.183
        delta_ = 2
        nbr_waves = 50
        car = [random.triangular(g_sharp_freq - delta_, g_sharp_freq + delta_) for i in range(nbr_waves)]
        rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
        self.fm = FM(carrier=car, ratio=rat, index=SigTo(0), mul=1.5 / nbr_waves).out()
        self.reader = Spectrum(self.fm, function=self.on_data)
        self.reader.polltime(self.frame_update)

    def example2_init_(self):
        """ self.b = Thresh(SigTo(0), threshold=[0.025], dir=2)
        self.env = CosTable([(0, 0.5), (100, 0.5), (1024, 0.5), (7000, 0.5), (8192, 0.5)])
        self.amp = TrigEnv(self.b, table=self.env, dur=0.5, mul=.3)
        self.scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
        self.freq = TrigChoice(self.b, self.scl) """

        self.freq = 440
        self.amp = 1

        self.sine = Sine(freq=[self.freq, self.freq], mul=self.amp * .5).out()
        self.sine2 = Sine(freq=[self.freq, self.freq], mul=self.amp * .5)

        g_sharp_freq = 277.183
        delta_ = 2
        nbr_waves = 50
        car = [random.triangular(g_sharp_freq - delta_, g_sharp_freq + delta_) for i in range(nbr_waves)]
        rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
        self.fm = FM(carrier=car, ratio=rat, index=SigTo(0), mul=1.5 / nbr_waves).out()

        self.reader = Spectrum(self.sine + self.fm, function=self.on_data)
        self.reader.polltime(self.frame_update)

        # self.src_output = Selector([self.sine, self.sine2, self.fm]).out()
        # self.fft_ = FFT(self.src_output)


    def example3_init_(self):
        # self.b = Thresh(SigTo(0), threshold=[0.2], dir=0)
        self.env = CosTable([(0, 0), (100, 0.5), (1024, 0.5), (7000, 0.5), (8192, 0)])
        # self.amp = TrigEnv(self.b, table=self.env, dur=1, mul=.6)
        self.amp = 0
        self.scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
        # self.freq = TrigChoice(self.b, self.scl)

        # self.sine = Sine(freq=[self.freq, self.freq], mul=self.amp * .5).out()
        # self.sine2 = Sine(freq=[self.freq, self.freq], mul=self.amp * .5).out(1)

        g_sharp_freq = 277.183
        delta_ = 2
        nbr_waves = 50
        car = [random.triangular(g_sharp_freq - delta_, g_sharp_freq + delta_) for i in range(nbr_waves)]
        rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
        self.fm = FM(carrier=car, ratio=rat, index=SigTo(0), mul=1.5 / nbr_waves).out()

        self.reader = Spectrum(self.fm, function=self.on_data)
        self.reader.polltime(self.frame_update)

    def example5_init_(self):
        self.b = Thresh(SigTo(0), threshold=[0.125], dir=2)
        self.env = CosTable([(0, 0), (100, 0.5), (1024, 0.5), (7000, 0.5), (8192, 0)])
        self.amp = TrigEnv(self.b, table=self.env, dur=0.5, mul=.3)
        self.scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
        self.freq = TrigChoice(self.b, self.scl)

        self.sine = Sine(freq=[self.freq, self.freq], mul=self.amp * .5).out()
        self.sine2 = Sine(freq=[self.freq, self.freq], mul=self.amp * .5).out(1)

        g_sharp_freq = 277.183
        delta_ = 2
        nbr_waves = 50
        car = [random.triangular(g_sharp_freq - delta_, g_sharp_freq + delta_) for i in range(nbr_waves)]
        rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
        self.fm = FM(carrier=car, ratio=rat, index=SigTo(0), mul=1.5 / nbr_waves).out()

        self.reader = Spectrum(self.sine + self.sine2 + self.fm, function=self.on_data)
        self.reader.polltime(self.frame_update)

    def get_spectrum_data(self, indata):
        """
        Override function from Pyo Spectrum function. It delivers the data as a list of lists
        Each list has the values for each stream.
        In each stream, a list of tuples with 512 samples represents the frequency magnitude of the signal:
        [(0, mag1), (1, mag2), (2, mag3), ... (512, mag512)]
        The frequency range goes from 0 to 22050 Hz (half the sampling frequency of the audio waveform).
        """
        x, y = zip(*indata[0])
        # print(self.x_index[-1])
        if (self.frame_cnt < self.num_frames):
            self.spec_buffer[self.frame_cnt, list(x)] = np.abs(np.max(y)-y)
            self.x_spec_buffer[self.frame_cnt] = self.x_index[-1]
            self.frame_cnt += 1
        else:
            self.spec_buffer[0:-1, :] = self.spec_buffer[1:, :]
            self.x_spec_buffer[0:-1] = self.x_spec_buffer[1:]
            self.spec_buffer[-1, list(x)] = np.abs(np.max(y) - y)
            self.x_spec_buffer[-1] = self.x_index[-1]
            self.frame_cnt += 1

        self.freq_buffer = np.abs(np.max(y)-y)

    def start(self):
        self.s.start()

    def stop(self):
        self.s.stop()


class BioSound():
    def __init__(self, mac="00:07:80:8C:AD:C9", fs=1000, example="example0", signal=["EMG"], n_frames=128):
        self.mac = mac
        self.fs = fs
        self.n_frames = n_frames  # size of buffer
        self.n_i = 0  # index in buffer
        self.arr = []
        self.push_buffer = np.zeros((self.n_frames, 1))  # configure buffer
        self.example = example
        self.signal = signal

    def setup(self):
        """
        Configures the NewDevice from BiosignalsPlux
        Configures the Pyo Sound Class
        :return:
        """
        self.sound = SoundGenerator(self.example)
        self.device = In_BiosignalsPlux(self.mac, freq=self.fs, signal=self.signal)  # biosignals device

    def start(self):
        # start pyo
        self.sound.start()
        # start bioplux
        if(self.example=="example0"):
            self.device._set_on_data(self.store_in_buffer)
        elif(self.example=="example1"):
            self.device._set_on_data(self.example1_ondata)
        elif(self.example=="example2"):
            self.device._set_on_data(self.example2_ondata)
        elif (self.example == "example3"):
            self.device._set_on_data(self.example3_ondata)
        elif (self.example == "example5"):
            self.device._set_on_data(self.example5_ondata)
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

    def store_buffer(self, data):
        if (self.n_i < self.n_frames):
            self.push_buffer[self.n_i, :] = self.device.transferFunction(data[0])
            self.n_i += 1
        else:
            self.push_buffer[0:-1, :] = self.push_buffer[1:, :]
            self.push_buffer[-1, :] = self.device.transferFunction(data[0])
            self.n_i += 1
    def example1_ondata(self, nseg, fn):
        #set thresold input
        print(self.device.transferFunction(fn[0]))
        self.sound.b.setInput(Sig(self.device.transferFunction(fn[0])))
    def example2_ondata(self, nseg, fn):
        self.store_buffer(fn)
        self.sound.b.setInput(Sig(self.device.transferFunction(fn[0])))
        self.sound.fm.setIndex(5*float(np.mean(np.abs(self.push_buffer))))

    def example3_ondata(self, nseg, fn):
        # self.store_buffer(fn)
        # self.sound.b.setInput(Sig(self.device.transferFunction(fn[0])))
        self.sound.fm.setIndex(10*Sig(self.device.transferFunction(fn[0])))
    def example5_ondata(self, nseg, fn):
        self.store_buffer(fn)
        env = float(np.mean(np.abs(self.push_buffer)))
        self.sound.b.setInput(Sig(2*env))
        self.sound.fm.setIndex(5*env)

    # def store_in_buffer(self, nseq, fn):
    #     # self.sound.freq_slider.value = 250
    #     # print(float(abs(self.device.transferFunction(fn))[0])/3.6)
    #     # self.sound.amp_slider.value = float(abs(self.device.transferFunction(fn))[0]/3.6)
    #     # print(t_in-self.device.t0)
    #     # print(nseq, t_in - self.device.t0)
    #     # self.arr.append(t_in - self.device.t0)
    #
    #     # print(self.device.transferFunction(fn[0]))
    #
    #     if (self.n_i < self.n_frames):
    #         self.push_buffer[self.n_i, :] = self.device.transferFunction(fn[0])
    #         # self.push_buffer[self.n_i, :] = fn[0]-32768
    #         self.n_i += 1
    #     else:
    #         self.push_buffer[0:-1, :] = self.push_buffer[1:, :]
    #         self.push_buffer[-1, :] = self.device.transferFunction(fn[0])
    #         # self.push_buffer[-1, :] = fn[0]-32768
    #         self.n_i += 1
    #
    #     # Experience 1
    #
    #     # Experience 2
    #
    #     # Experience 3
    #
    #     # Experience 4
    #
    #     # if(nseq%500==0):
    #     # amp_ = len(self.sound.scl) * np.mean(np.abs(self.push_buffer))
    #     # print(self.sound.scl[int(amp_)])
    #     # self.sound.scl_ind.value = self.sound.scl[int(amp_)]
    #     amp = abs(self.device.transferFunction(fn[0])) / 1.5
    #     # amp = 1000*float(np.mean(abs(self.push_buffer)))
    #     # print(amp)
    #     # self.sound.osc.setFreq(100+float(500*amp))
    #
    #     # self.sound.scl_ind = self.sound.scl[2*int(amp_)]
    #     # print(self.sound.scl[2*int(amp_)])
    #     # amp_ = 250*np.abs(self.device.transferFunction(fn[0]))/3.6
    #     # self.sound.osc.setFreq(midiToHz(self.sound.scl[int(amp_)]))
    #     # self.sound.osc.setFreq(440 + int(amp**1.5))
    #
    #     # self.sound.osc.setMul(250 + int(5*amp_))
    #     # self.sound.freq_slider.value =


if __name__ == "__main__":
    session = BioSound()
    session.setup()
    session.start()
    session.stop()
