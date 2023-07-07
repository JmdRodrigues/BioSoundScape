import time

from pyo import *
from tools.plux_device import In_BiosignalsPlux
from tools.processing_tools import *

import numpy as np

import json

def noop():
    pass

class SoundGenerator():
    def __init__(self, plot_duration=3, update_spectrum_interval=0.05, on_data=noop, on_data_audio=noop):
        self.s = Server().boot()
        self.duration = plot_duration  # Recording duration in seconds
        self.audio_plot_duration = 0.0001 #in seconds
        # sample_rate = 44100  # Sample rate (adjust if necessary)
        # self.frame_update = update_spectrum_interval
        self.frame_update = 0.1
        # Initialize the recording buffer
        self.num_frames = int(self.duration//self.frame_update)
        # self.spec_buffer = np.zeros((self.num_frames, 512))
        # self.x_spec_buffer = np.zeros(self.num_frames)
        # self.freq_buffer = np.zeros(512)
        self.frame_cnt = 0

        self.notes_octaves_dict = self.load_notes()

        self.experiences_init = {"experience1": self.experience1_init, "experience2": self.experience2_init, "experience3": self.experience3_init, "experience4": self.experience4_init, "experience5": self.experience5_init, "experience6": self.experience6_init, "experience7": self.experience7_init, "experience8":self.experience8_init}
        self.audioTFs = {"experience1":self.audioTF1, "experience2":self.audioTF2, "experience3":self.audioTF3, "experience4":self.audioTF4, "experience5":self.audioTF5, "experience6":self.audioTF6, "experience7":self.audioTF7, "experience8":self.audioTF8}
        # self.experiences = {"experience1":self.experience1, "experience2":self.experience2, "experience3":self.experience3}

        self.on_data = on_data
        self.on_data_audio = on_data_audio

        if(example=="experience1"):
            """
            Experience 1-a:
            EMG envelope changes frequency of pure sine wave
            """
            self.experience1_init()
        elif(example == "experience2"):
            """
            Experience 2-a:
            EMG envelope changes increases octaves of the same key note
            """
            self.experience2_init()
        elif (example == "experience3"):
            """
            TBD
            """
            self.experience3_init()
        elif (example == "experience4"):
            """
            Experience 4-a:
            Drone Sound intensity varies with EMG envelope and also increases the keys in a pentatonic scale
            """
            self.experience4_init()
        elif (example == "experience5"):
            """
            Experience 5-a:
            ECG wave modulating drone sound
            """
            self.experience5_init()
        elif (example == "experience6"):
            """
            Experience 6-a:
            ECG wave modulating drone sound.
            Peak detector identifies peaks and plays a key in a specific sound.
            """
            self.experience6_init()
        elif (example == "experience7"):
            """
            Experience 7-a:
            EDA wave modulating drone sound.
            """
            self.experience7_init()

    def load_notes(self):
        with open('../../data/notes_octaves.json') as file:
            # Load the JSON data into a Python data structure
            data = json.load(file)
        return data

    def experience1_init(self):
        """
        Using EMG envelope to change the frequency of a sine wave
        """
        t = HarmTable([1, 0.33, .2, 0.1])

        amp = TableRead(table=t, freq=440, loop=True, mul=0.3)
        # rat = TableRead(table=rat_table, freq=1, loop=True)
        ind = TableRead(table=t, freq=1, loop=True)

        self.sine = Osc(table=t, freq=[440, 440], mul=.2).out()
        self.sine = FM(carrier=[440, 440], ratio=.1, index=ind, mul=.2).out()
        # self.sine = Sine(freq=440, mul=.3).out()
        self.reader = Spectrum(self.sine, function=self.on_data)
        self.audio_reader = Scope(self.sine, function=self.on_data_audio)
        self.reader.polltime(self.frame_update)
        self.audio_reader.setLength(self.audio_plot_duration)

    def experience2_init(self):
        """
        Using EMG envelope to change the octave of a set of sine waves.
        The Voice parameter ranges from [0 - self.sel_size].
        self.sel_size is the number of sine waves in the selector.
        Each sine wave has a single frequency of 440*(2**octave), being octave the position of the corresponding sine in the
        selector.
        As the amplitude of the EMG envelope increases, the selector combines the set of sine waves presence.
        """
        self.sel_size = 5
        self.sel = Selector([Sine(freq=(2**i)*440, mul=.3) for i in range(self.sel_size)]).out()
        self.reader = Spectrum(self.sel, function=self.on_data)
        self.audio_reader = Scope(self.sel, function=self.on_data_audio)
        self.reader.polltime(self.frame_update)
        self.audio_reader.setLength(self.audio_plot_duration)

    def experience3_init(self):
        """
        Using EMG to augment the intensity of an FM wave
        """
        g_sharp_freq = 277.183
        delta_ = 2
        nbr_waves = 25
        car = [random.triangular(g_sharp_freq - delta_, g_sharp_freq + delta_) for i in range(nbr_waves)]
        rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
        ind = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
        # rat = [random.choice([.1, .2, .25, .5, .75, 1]) for i in range(nbr_waves)]
        self.fm = FM(carrier=car, ratio=rat, index=ind, mul=0.075 / nbr_waves).out()
        self.reader = Spectrum(self.fm, function=self.on_data)
        self.audio_reader = Scope(self.fm, function=self.on_data_audio)
        self.reader.polltime(self.frame_update)
        self.audio_reader.setLength(self.audio_plot_duration)

    def experience4_init(self):
        """
        Using EMG to augment the intensity of an FM wave, while also having a threshold to detect when to play a key
        """
        self.phasor = Phasor(1)
        self.b = Thresh(self.phasor, threshold=[0.5], dir=0)
        self.env = CosTable([(0, 0.0), (64, 0.2), (128, 0.4), (1024, 0.65), (6200, 0.4), (7000, 0.2), (8192, 0.0)])
        self.amp = TrigEnv(self.b, table=self.env, dur=2, mul=.3)
        self.scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
        self.sel_size = len(self.scl)
        # self.freq = TrigChoice(self.b, self.scl)
        self.trig_func = TrigFunc(self.b, self.choose_key)
        self.val = SigTo(0)
        self.freq = SigTo(self.scl[self.val.value])
        self.sine = Sine(freq=[self.freq, self.freq], mul=self.amp * .25).out()

        g_sharp_freq = 277.183 #in Hz
        delta_ = 2
        nbr_waves = 25
        car = [random.triangular(g_sharp_freq - delta_, g_sharp_freq + delta_) for i in range(nbr_waves)]
        rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
        # rat = [random.choice([.1, .2, 0.25, 0.5, 0.75, 1]) for i in range(nbr_waves)]
        self.fm = FM(carrier=car, ratio=rat, index=SigTo(0), mul=0.25 / nbr_waves).out()

        self.reader = Spectrum(self.sine+self.fm, function=self.on_data)
        self.audio_reader = Scope(self.sine+self.fm, function=self.on_data_audio)
        self.reader.polltime(self.frame_update)
        self.audio_reader.setLength(self.audio_plot_duration)

    def experience5_init(self):
        """
        Using ECG to augment the intensity of an FM wave
        """
        # self.b = Thresh(SigTo(0), threshold=[0.5], dir=0)
        # self.env = LinTable([(0,0), (190,.8), (1000,.5), (4300,.1), (8191,0)], size=8192)
        # self.amp = TrigEnv(self.b, table=self.env, dur=1, mul=.3)
        #
        # self.scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
        # self.sel_size = len(self.scl)
        # self.freq = TrigChoice(self.b, self.scl)
        # self.sine = Sine(freq=[self.freq, self.freq], mul=self.amp * .1).out()

        g_sharp_freq = 277.183 #in Hz
        delta_ = 2
        nbr_waves = 10
        car = [random.triangular(g_sharp_freq - delta_, g_sharp_freq + delta_) for i in range(nbr_waves)]
        rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
        # rat = [random.choice([.1, .2, 0.25, 0.5, 0.75, 1]) for i in range(nbr_waves)]
        self.fm = FM(carrier=car, ratio=rat, index=SigTo(0), mul=.025/nbr_waves).out()

        self.reader = Spectrum(self.fm, function=self.on_data)
        self.audio_reader = Scope(self.fm, function=self.on_data_audio)
        self.reader.polltime(self.frame_update)
        self.audio_reader.setLength(self.audio_plot_duration)

    def experience6_init(self):
        """
        Using ECG to augment the intensity of an FM wave and detecting the peak of the ECG
        """
        self.b = Thresh(SigTo(0), threshold=[0.75], dir=0)
        self.env = LinTable([(0, 0), (190, .01), (560, .1), (1000, .5), (4300, .1), (7600, .01), (8191, 0)], size=8192)
        self.amp = TrigEnv(self.b, table=self.env, dur=1, mul=.5)

        self.scl = [midiToHz(i) for i in EventScale(root="G#", scale="majorPenta", first=4, octaves=2, type=0)]
        self.sel_size = len(self.scl)
        self.freq = TrigChoice(self.b, self.scl)
        self.sine = Sine(freq=[self.freq, self.freq], mul=self.amp * .2).out()

        g_sharp_freq = 277.183  # in Hz
        delta_ = 2
        nbr_waves = 10
        car = [random.triangular(g_sharp_freq - delta_, g_sharp_freq + delta_) for i in range(nbr_waves)]
        rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
        # rat = [random.choice([.1, .2, 0.25, 0.5, 0.75, 1]) for i in range(nbr_waves)]
        self.fm = FM(carrier=car, ratio=rat, index=SigTo(0), mul=.005).out()

        self.reader = Spectrum(self.sine + self.fm, function=self.on_data)
        self.audio_reader = Scope(self.sine + self.fm, function=self.on_data_audio)
        self.reader.polltime(self.frame_update)
        self.audio_reader.setLength(self.audio_plot_duration)

    def experience7_init(self):
        """
        Using EMG to augment the intensity of an FM wave, while also having a threshold to detect when to play a key
        """
        t = HarmTable([1, 0, .33, 0, .2, 0, .143, 0, .111])
        self.sine = Osc(table=t, freq=[440, 440], mul=.2).out()
        # self.sine = Sine(freq=440, mul=.3).out()
        self.reader = Spectrum(self.sine, function=self.on_data)
        self.audio_reader = Scope(self.sine, function=self.on_data_audio)
        self.reader.polltime(self.frame_update)
        self.audio_reader.setLength(self.audio_plot_duration)

    def experience8_init(self):
        """
        Using EMG to augment the intensity of an FM wave, while also having a threshold to detect when to play a key
        """
        t = HarmTable([1, 0, .33, 0, .2, 0, .143, 0, .111])
        self.sine = Osc(table=t, freq=[440, 440], mul=.05).out()
        # self.sine = Sine(freq=440, mul=.3).out()
        self.reader = Spectrum(self.sine, function=self.on_data)
        self.audio_reader = Scope(self.sine, function=self.on_data_audio)
        self.reader.polltime(self.frame_update)
        self.audio_reader.setLength(self.audio_plot_duration)

    def experience9_init(self):
        """
        Using EMG to augment the intensity of an FM wave, while also having a threshold to detect when to play a key
        """
        t = HarmTable([1, 0, .33, 0, .2, 0, .143, 0, .111])
        self.sine = Osc(table=t, freq=[440, 440], mul=.05).out()
        # self.sine = Sine(freq=440, mul=.3).out()
        self.reader = Spectrum(self.sine, function=self.on_data)
        self.audio_reader = Scope(self.sine, function=self.on_data_audio)
        self.reader.polltime(self.frame_update)
        self.audio_reader.setLength(self.audio_plot_duration)


    def choose_key(self):
        self.freq.setValue(self.scl[int(self.val.value)])
    def audioTF1(self, sig):
        max_ = 0.3 #EMG max value
        return scale_freq(tf_tanh_audio(sig, max_))

    def audioTF2(self, sig):
        max_ = 0.3  # EMG max value
        return scale_voice(tf_tanh_audio(sig, max_), self.sel_size)

    def audioTF3(self, sig):
        max_ = 0.001 #EMG max value
        out_ = scale_freq(tf_tanh_audio(sig, max_))
        return out_

    def audioTF4(self, sig):
        max_ = 0.3  # EMG max value
        return 10*scale_index(tf_tanh_audio(sig, max_))

    def audioTF5(self, sig):
        sig = (sig + 1.47)/(2*1.47)
        # print(sig)
        max_ = 0.5 #ECG max
        out = sig
        # print(out)
        return scale_index(2.5*out)

    def audioTF6(self, sig):
        sig = (sig + 1.47) / (2 * 1.47)
        out = 2*sig
        return scale_index(out)

    def audioTF7(self, sig):
        max_ = 25
        return scale_freq(scale(sig-0.5, max_), octave=2)

    def audioTF8(self, sig):
        max_ = 1.47
        sig = (sig + 1.47) / (2 * 1.47)
        print(sig)
        return scale_freq(abs(sig)/10)

    def audioTF9(self, sig):
        max_ = 1.47
        sig = (sig + 1.47) / (2 * 1.47)
        print(sig)
        return scale_freq(abs(sig)/10)

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

        keys = list(self.notes_octaves_dict.keys())
        # sines = [Sine(freq=[self.notes_octaves_dict[key][3], self.notes_octaves_dict[key][3]], mul=self.amp * .5) for key in keys]
        sines = [Sine(freq=[freq_i, freq_i], mul=.3) for freq_i in self.notes_octaves_dict[keys[1]]]
        self.sel = Selector(sines).out()
        # self.sine = Sine(freq=[self.freq, self.freq], mul=self.amp * .5)
        # self.sine2 = Sine(freq=[self.freq, self.freq], mul=self.amp * .5)

        g_sharp_freq = 277.183
        delta_ = 2
        nbr_waves = 50
        car = [random.triangular(g_sharp_freq - delta_, g_sharp_freq + delta_) for i in range(nbr_waves)]
        rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(nbr_waves)]
        self.fm = FM(carrier=car, ratio=rat, index=SigTo(0), mul=1.5 / nbr_waves)

        self.reader = Spectrum(self.sel, function=self.on_data)
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

    def get_audio_data(self, indata):
        """
        Override function from Pyo Scope function. It delivers the data as a list of lists
        Each list has the values for each stream.
        In each stream, a list of tuples with 512 samples represents the frequency magnitude of the signal:
        [(0, samp1), (1, samp2), (2, samp3), ... (512, samp4)]
        The signal length is dependent on the duration that was selected for the buffer
        """



        x, y = zip(*indata[0])
        self.audio_buffer = y

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
    def __init__(self, mac="00:07:80:8C:AD:C9", example= "example0", fs=1000, signal=["EMG"], n_frames=128):
        self.mac = mac
        self.fs = fs
        self.n_frames = n_frames  # size of buffer
        self.n_i = 0  # index in buffer
        self.arr = []
        self.push_buffer = np.zeros((self.n_frames, 1))  # configure buffer
        self.example = example
        self.signal = signal
        self.max = 0
        self.min = 100000000000000

    def on_data_print(self, nseq, fn):
        self.store_buffer(fn)
        val = np.mean(np.abs(self.push_buffer))
        if(self.max < val):
            self.max = val
            print("MAX:")
            print(self.max)

        if(self.min > val):
            self.min = val
            print("MIN:")
            print(self.min)

    def setup(self):
        """
        Configures the NewDevice from BiosignalsPlux
        Configures the Pyo Sound Class
        :return:
        """
        if(self.example=="0"):
            self.device = In_BiosignalsPlux(self.mac, freq=self.fs, signal=self.signal)  # biosignals device
        else:
            self.sound = SoundGenerator(self.example)
            self.device = In_BiosignalsPlux(self.mac, freq=self.fs, signal=self.signal)  # biosignals device


    def start(self):
        # start pyo
        if(self.example=="0"):
            self.device._set_on_data(self.on_data_print)
        else:
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

        #start bioplux device
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
    session = BioSound(example="0", signal=["ACC_X"])
    session.setup()
    session.start()
    time.sleep(60)
    session.stop()
