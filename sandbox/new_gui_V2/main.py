import sys
import platform
import json
import time
import sched

from pyo import SigTo
from novainstrumentation import lowpass

sys.path.insert(1, "../../")

import numpy as np

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
import pyqtgraph as pg

## ==> Multiprocessing
import multiprocessing as mp

## ==> SPLASH SCREEN
from ui_intro_loader import Ui_LoadingScreen

## ==> MAIN WINDOW
from ui_main import Ui_MainWindow

## ==> MAIN QSS STYLES
# IMPORT QSS CUSTOM
# from styles.ui_styles import Style

## ==> Biosignals and Sonification Tools
from tools.plux_device import In_BiosignalsPlux
from tools.sonification import SoundGenerator
from tools.plot_tools import customColormap

## ==> GLOBALS
counter = 0


class Biosignals():
    def __init__(self, mac, sr, buffer_size, biosig_type):
        print("MAC:")
        print(mac)
        self.buffer_size = buffer_size
        self.mac = mac
        self.sr = sr

        self.signal = biosig_type

        self.n_i = 0

        self.shared_index = mp.RawArray('d', range(self.buffer_size))
        self.shared_values = mp.RawArray('d', np.zeros(self.buffer_size))
        
        self.plux_connected = mp.RawValue('i', 0)

    def run(self, biosig_type, stop_event):
        cnt_ = 0
        while cnt_ <= 3:
            try:
                # print("trying to connect with bioplux device")
                self.device = In_BiosignalsPlux(self.mac, freq=self.sr, on_data=self.receive_buffer, signal=biosig_type)
                self.plux_connected.value = 1
                print("Bioplux device connected. Launching acquisition...")
                break
            except:
                if(cnt_<3):
                    cnt_+=1
                    print(cnt_)
                else:
                    print("Error: Device could not be connected. Check battery, status or mac address...")
                    break
                    # self._close() #TODO: define closing method for the entire app
        if(self.plux_connected.value == 1):
            self.device._onstart()


    def receive_buffer(self, nseq, fn):
        if (self.n_i < self.buffer_size):
            self.shared_index[self.n_i] = nseq
            self.shared_values[self.n_i] = self.device.transferFunction(fn[0])
            self.n_i += 1
        else:
            self.shared_index[0:-1] = self.shared_index[1:]
            self.shared_values[0:-1] = self.shared_values[1:]
            self.shared_index[-1] = nseq
            self.shared_values[-1] = self.device.transferFunction(fn[0])
            self.n_i += 1
        
        if(self.event.is_set()):
            self.device._onstop()
        

    def launch_biosignals(self):
        """
            source: launch app for streaming OpenSignals Data
        """
        self.event = mp.Event()
        self.process = mp.Process(
            name='biosignalsplux',
            target=self.run,
            args=[self.signal, self.event]
        )
        self.process.start()
    
    def terminate_biosignal(self):
        self.event.set()
        time.sleep(0.25)
        self.process.terminate()
        self.process.join()

class Sound():
    #TODO: we still need to verify why some beeps appear in the output sound. I noticed it is related with some blocking mechanism in the processing stage. 
    def __init__(self, plot_duration, spectrum_update, num_frames, shared_array):
    # def __init__(self, plot_duration, spectrum_update, num_frames):
        self.plot_duration = plot_duration
        #self.spectrum_update = spectrum_update
        self.spectrum_update = 0.1
        self.num_frames = num_frames
        
        # Initialize the recording buffer
        self.audio_frame_cnt = 0
        self.frame_cnt = 0  # initialized frame cnt
        self.shared_spec_buffer = mp.RawArray('d', np.zeros(self.num_frames * 500))
        # print(self.shared_spec_buffer)
        self.shared_freq_buffer = mp.RawArray('d', np.zeros(512))
        self.shared_audio_buffer = mp.RawArray('d', np.zeros(500)) #every tenth of a second, comes a 512 samples packet

        self.sound_connected = mp.RawValue('i', 0)
        self.shared_modulator = shared_array
    
        # print(self.shared_modulator)

    def run(self, experience, event):
        self.sound = SoundGenerator(self.plot_duration, self.spectrum_update, on_data=self.receive_buffer, on_data_audio=self.receive_audio_buffer)
        self.sound.start()
        self.sound_connected.value = 1

        self.experience = experience

        self.init_modulation()

        while not event.is_set():
            pass
        self.stop()
    
    def stop(self):
        self.scheduler.cancel()
        self.sound.stop()

    def receive_audio_buffer(self, indata):
        x, y = zip(*indata[0])
        self.shared_audio_buffer[:len(y)] = y
        # if (self.audio_frame_cnt < self.plot_duration):
        #     self.shared_audio_buffer[self.audio_frame_cnt * len(y):(self.audio_frame_cnt * len(y)) + len(y)] = y
        #     self.audio_frame_cnt += 1
        # else:
        #     self.shared_audio_buffer[0:-len(y)] = self.shared_audio_buffer[len(y):]
        #     self.shared_audio_buffer[-len(y):] = y
        #     # self.x_spec_buffer[-1] = self.x_index[-1]
        #     self.audio_frame_cnt += 1

    def receive_buffer(self, indata):
        x, y = zip(*indata[0])
        # print(self.x_index[-1])
        if (self.frame_cnt < self.num_frames):
            self.shared_spec_buffer[self.frame_cnt * 500:self.frame_cnt * 500 + len(y[:500])] = np.abs(np.max(y[:500]) - y[:500])
            self.frame_cnt += 1
        else:
            self.shared_spec_buffer[0:-500] = self.shared_spec_buffer[500:]
            self.shared_spec_buffer[-500:] = np.abs(np.max(y[:500]) - y[:500])
            # self.x_spec_buffer[-1] = self.x_index[-1]
            self.frame_cnt += 1

        self.shared_freq_buffer[:len(y)] = np.abs(np.max(y) - y)

    def init_modulation(self):
        print("init_modulation")
        #modulate audio signal
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.modulation_interval = 10 #in milliseconds


        #call init experience3
        print(self.experience)
        self.sound.experiences_init[self.experience]()

        self.experiences = {"experience1": self.experience1, "experience2": self.experience2, "experience3": self.experience3, "experience4": self.experience4, "experience5": self.experience5, "experience6": self.experience6, "experience7": self.experience7, "experience8": self.experience8}

        #set callback experience
        self.scheduler.enter(self.modulation_interval/1000, 1, self.experiences[self.experience])
        self.scheduler.run()

    def experience1(self):
        self.scheduler.enter(self.modulation_interval / 1000, 1, self.experience1)
        env = np.mean(np.abs(self.shared_modulator))
        # self.sound.sine.setFreq(float(self.sound.audioTF1(env)))
        self.sound.sine.setCarrier([float(self.sound.audioTF1(env)),float(self.sound.audioTF1(env))])

    def experience2(self):
        self.scheduler.enter(self.modulation_interval / 1000, 1, self.experience2)
        env = np.mean(np.abs(self.shared_modulator))
        self.sound.sel.setVoice(float(self.sound.audioTF2(env)))

    def experience3(self):
        self.scheduler.enter(self.modulation_interval / 1000, 1, self.experience3)
        # env = np.mean(np.abs(self.shared_modulator))
        self.sound.fm.setCarrier(float(self.sound.audioTF3(np.mean(self.shared_modulator))))
        # print(self.shared_modulator[0])
        # self.sound.fm.setIndex(float(abs(self.shared_modulator[0])/20))

    def experience4(self):
        self.scheduler.enter(self.modulation_interval / 1000, 1, self.experience4)
        env = np.mean(np.abs(self.shared_modulator))

        self.sound.val.setValue(float(self.sound.audioTF2(2*env)))
        self.sound.fm.setIndex(float(self.sound.audioTF4(env)))

    def experience5(self):
        self.scheduler.enter(self.modulation_interval / 1000, 1, self.experience5)
        # env = 25*np.mean(np.abs(np.diff(self.shared_modulator)))
        # print(env)
        # env = self.shared_modulator[0]
        # print(env)
        # self.sound.b.setInput(SigTo(float(env)))
        # self.sound.fm.setIndex(float(self.sound.audioTF5(2*self.shared_modulator[0])))
        self.sound.fm.setIndex(float(self.sound.audioTF5(np.mean(self.shared_modulator[:5]))))
        # print(self.shared_modulator[0])
        # self.sound.fm.setIndex(float(self.sound.audioTF5(self.shared_modulator[0])))
        # self.sound.fm.setIndex(float(self.sound.audioTF5(env/25)))

    def experience6(self):
        self.scheduler.enter(self.modulation_interval / 1000, 1, self.experience6)

        beat_ = np.mean(np.abs(np.diff(self.shared_modulator[:5])))
        self.sound.b.setInput(SigTo(float(beat_*50)))
        print(30*beat_)
        self.sound.fm.setIndex(float(self.sound.audioTF5(np.mean(self.shared_modulator[:10]))))

    def experience7(self):
        print(self.shared_modulator[0])
        self.scheduler.enter(self.modulation_interval / 1000, 1, self.experience7)
        self.sound.sine.setFreq(float(self.sound.audioTF7(np.mean(self.shared_modulator))))

    def experience8(self):
        print(self.shared_modulator[0])
        self.scheduler.enter(self.modulation_interval / 1000, 1, self.experience8)
        self.sound.sine.setFreq(float(self.sound.audioTF8(np.mean(self.shared_modulator[:10]))))

    # def audioAmplitudeModulator(self):
    #     """Modulate Audio Amplitude output with direct value of signal"""
    #     # print("modulating...")
    #     self.scheduler.enter(self.modulation_interval/1000, 1, self.audioAmplitudeModulator)
    #     # self.sound.b.setInput(Sig(float(np.mean(np.abs(self.y_data)))))
    #     # self.sound.fm.setIndex(self.shared_modulator[-1])
    #     # self.sound.sine.setFreq(440 + int((100*float(np.mean(np.abs(self.shared_modulator))))**2))
    #     # self.sound.sel.setVoice(5*float(np.mean(np.abs(self.shared_modulator))))
    #     self.sound.sel.setVoice(20*abs(self.shared_modulator[0]))
    #     # self.sound.sine.setMul(0.005 + float(np.abs(self.shared_modulator[0])))
    #     # self.worker.sound.sine.setFreq(440+float(np.sum(np.abs(self.y_data))))

    # def audioModulator_example1(self):
    #     """Modulate Audio"""
    #     # print("modulating...")
    #     self.scheduler.enter(self.modulation_interval/1000, 1, self.audioModulator)
    #     # self.sound.b.setInput(Sig(float(np.mean(np.abs(self.y_data)))))
    #     self.sound.fm.setIndex(10*float(np.std(np.abs(self.shared_modulator))))
    #     self.sound.sine.setFreq(440 + int((100*float(np.mean(np.abs(self.shared_modulator))))**2))
    #     # self.worker.sound.sine.setFreq(440+float(np.sum(np.abs(self.y_data))))

    def launch_sound(self, experience):
        """
        source: launch app for streaming Audio Data
        """
        self.event = mp.Event()
        self.process = mp.Process(
            name='sound',
            target=self.run,
            args=[experience, self.event]
        )
        self.process.start()

    def terminate_sound(self):
        self.event.set()
        time.sleep(0.25)
        self.process.terminate()
        self.process.join()

# YOUR APPLICATION
class MainWindow(QMainWindow):
    def __init__(self, intro_ui, current_example_id):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.intro_ui = intro_ui

        self.intro_ui.pushButton_Stop.clicked.connect(self.StopAcquisition)
        self.current_example_id = current_example_id

        self.launch_cntr = 0

        self.LaunchAcquisition()


    def configurePlots(self):
        self.plot_duration = 10 #in seconds
        self.signal_frame_update = 0.015 #in seconds
        self.image_frame_update = 0.1 #in seconds
        self.signal_plot_size = int(self.plot_duration*self.sr)
        self.num_signal_frames = int(self.plot_duration // self.signal_frame_update) #for spectogram computation
        self.num_image_frames = int(self.plot_duration // self.image_frame_update) #for spectogram computation

        self.x_plot = np.zeros(self.signal_plot_size)
        self.y_plot = np.zeros(self.signal_plot_size)

        if(self.launch_cntr == 0):
            self.init_plots()
        else:
            self.reset_plots()

    def updateButtonsStatesStop(self):
        self.intro_ui.pushButton_Stop.setEnabled(True)
        self.intro_ui.pushButton_Launch.setEnabled(True)
        self.intro_ui.comboBox_examples.setEnabled(True)
        self.intro_ui.textEdit_signalType.setDisabled(True)
        self.intro_ui.textEdit_mac_address.setDisabled(True)
        self.intro_ui.textEdit_sampling_rate.setDisabled(True)
        self.intro_ui.textEdit_buffer_size.setDisabled(True)

    def init_biosignal_plot(self):
        # Create the pyqtgraph window
        self.layout_biosig = QGridLayout()
        self.graphWidget_biosig = pg.PlotWidget()
        self.layout_biosig.addWidget(self.graphWidget_biosig)
        self.graphWidget_biosig.plot()
        self.graphWidget_biosig.enableAutoRange(x=True, y=True)
        self.graphWidget_biosig.showGrid(x=True, y=False, alpha=0.3)
        self.graphWidget_biosig.setXRange(0, self.plot_duration)
        # self.graphWidget_biosig
        self.graphWidget_biosig.setBackground("#545454")
        self.graphWidget_biosig.setLabel("left", "Amplitude (n.a.)")
        self.graphWidget_biosig.setLabel("bottom", "Time (s)")
        # Set Range
        self.graphWidget_biosig.getPlotItem().hideAxis("bottom")
        self.graphWidget_biosig.getPlotItem().hideAxis("left")
        self.graphWidget_biosig.getPlotItem().setTitle("Biosignal")

        self.graphWidget_biosig.getAxis("left").setTextPen("w")
        # set size layout
        self.graphWidget_biosig.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        #add to Frame GraphWidget
        self.ui.graphBiosignal.setLayout(self.layout_biosig)

        self.graphWidget_biosig.clear()
        # restart the graph so that a new motion instance is created and the last one is forgot
        self.x = np.linspace(0, self.plot_duration, self.plot_duration*self.sr)
        self.y = np.zeros(self.plot_duration*self.sr)
        colors = ["w", "dodgerblue", "k", "orange", "mediumseagreen", "slateblue", "violet"]
        self.curves_biosig = [pg.PlotCurveItem(x=self.x, y=self.y, autoDownsample=True, antialias=True,
                                               pen=pg.mkPen(colors[0], width=2)) for i in range(self.nbr_channels)]

        for i, curve in enumerate(self.curves_biosig):
            self.graphWidget_biosig.addItem(curve)

    def init_biosignal_thumbnail_plot(self):
        # Create the pyqtgraph window
        self.layout_biosig_thumb = QGridLayout()
        self.graphWidget_biosig_thumb = pg.PlotWidget()
        self.layout_biosig_thumb.addWidget(self.graphWidget_biosig_thumb)
        self.graphWidget_biosig_thumb.plot()
        self.graphWidget_biosig_thumb.enableAutoRange(x=True, y=True)
        self.graphWidget_biosig_thumb.showGrid(x=True, y=False, alpha=0.3)
        self.graphWidget_biosig_thumb.setXRange(0, self.plot_duration)
        self.graphWidget_biosig_thumb.setYLink(self.graphWidget_biosig)
        # self.graphWidget_biosig
        self.graphWidget_biosig_thumb.setBackground("#545454")
        self.graphWidget_biosig_thumb.setLabel("left", "Amplitude (n.a.)")
        self.graphWidget_biosig_thumb.setLabel("bottom", "Time (s)")
        # Set Range
        self.graphWidget_biosig_thumb.getPlotItem().hideAxis("bottom")
        self.graphWidget_biosig_thumb.getPlotItem().hideAxis("left")
        self.graphWidget_biosig_thumb.getPlotItem().setTitle("Biosignal Snippet")

        self.graphWidget_biosig_thumb.getAxis("left").setTextPen("w")
        # set size layout
        self.graphWidget_biosig_thumb.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        #add to Frame GraphWidget
        self.ui.graphBiosignalThumbnail.setLayout(self.layout_biosig_thumb)

        self.graphWidget_biosig_thumb.clear()
        # restart the graph so that a new motion instance is created and the last one is forgot
        self.x = np.linspace(0, 1, 1*self.sr)
        self.y = np.zeros(1*self.sr)
        colors = ["w", "dodgerblue", "k", "orange", "mediumseagreen", "slateblue", "violet"]
        self.curves_biosig_thumb = [pg.PlotCurveItem(x=self.x, y=self.y, autoDownsample=True, antialias=True,
                                               pen=pg.mkPen(colors[0], width=2)) for i in range(self.nbr_channels)]

        for i, curve in enumerate(self.curves_biosig_thumb):
            self.graphWidget_biosig_thumb.addItem(curve)

    def init_sound_plot(self):
        # Create the pyqtgraph window
        self.layout_sound = QGridLayout()
        self.graphWidget_sound = pg.PlotWidget()
        self.layout_sound.addWidget(self.graphWidget_sound)
        self.graphWidget_sound.plot()
        self.graphWidget_sound.enableAutoRange(x=False, y=True)
        self.graphWidget_sound.showGrid(x=True, y=False, alpha=0.2)
        self.graphWidget_sound.setBackground("#545454")

        self.graphWidget_sound.getPlotItem().hideAxis("left")
        self.graphWidget_sound.getPlotItem().hideAxis("bottom")
        self.graphWidget_sound.getPlotItem().setTitle("FFT")
        # self.graphWidget_sound.getPlotItem().setLabel("bottom", "Frequency", units="Hz")

        # self.graphWidget_biosig.getAxis("left").setTextPen("w")

        self.graphWidget_sound.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        self.ui.graphSound.setLayout(self.layout_sound)

        self.graphWidget_sound.clear()
        # restart the graph so that a new motion instance is created and the last one is forgot
        self.x = np.linspace(0, 511, 512)
        self.y = np.zeros(512)
        colors = ["w", "dodgerblue", "k", "orange", "mediumseagreen", "dodgerblue", "slateblue", "violet"]
        self.curves_audio = [pg.PlotCurveItem(x=self.x, y=self.y, autoDownsample=True, antialias=True,
                                              pen=pg.mkPen(colors[0], width=2)) for i in range(self.nbr_channels)]

        for i, curve in enumerate(self.curves_audio):
            self.graphWidget_sound.addItem(curve)

    def init_audio_plot(self):
        # Create the pyqtgraph window
        self.layout_soundwave = QGridLayout()
        self.graphWidget_soundwave = pg.PlotWidget()
        self.layout_soundwave.addWidget(self.graphWidget_soundwave)
        self.graphWidget_soundwave.plot()
        self.graphWidget_soundwave.enableAutoRange(x=False, y=True)
        self.graphWidget_soundwave.showGrid(x=True, y=False, alpha=0.2)
        self.graphWidget_soundwave.setBackground("#545454")

        self.graphWidget_soundwave.getPlotItem().hideAxis("left")
        self.graphWidget_soundwave.getPlotItem().hideAxis("bottom")
        self.graphWidget_soundwave.getPlotItem().setTitle("Audio Wave")
        # self.graphWidget_sound.getPlotItem().setLabel("bottom", "Frequency", units="Hz")

        self.graphWidget_soundwave.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        self.ui.graphAudio_Thumbnail.setLayout(self.layout_soundwave)

        self.graphWidget_soundwave.clear()
        # restart the graph so that a new motion instance is created and the last one is forgot
        self.x = np.linspace(0, 511, 512)
        self.y = np.zeros(512)
        colors = ["w", "dodgerblue", "k", "orange", "mediumseagreen", "dodgerblue", "slateblue", "violet"]
        self.curves_audiowave = [pg.PlotCurveItem(x=self.x, y=self.y, autoDownsample=True, antialias=True,
                                              pen=pg.mkPen(colors[0], width=2)) for i in range(self.nbr_channels)]

        for i, curve in enumerate(self.curves_audiowave):
            self.graphWidget_soundwave.addItem(curve)

    def init_spectogram_plot(self):
        # Create the pyqtgraph window
        self.layout_spec = QGridLayout()
        self.view = pg.GraphicsLayoutWidget()
        self.layout_spec.addWidget(self.view)
        self.plot = self.view.addPlot()
        self.plot.setTitle("Spectrogram")
        self.view.setBackground("#545454")
        self.spec_item = pg.ImageItem()
        self.plot.addItem(self.spec_item)
        # self.layout_spec.addWidget(self.graphWidget_spec)
        # Convert a matplotlib colormap into a list of (tickmark, (r,g,b)) tuples
        colors_, pos = customColormap()
        self.list_cmpas = pg.colormap.listMaps()
        self.cm_ = pg.ColorMap(pos=pos, color=colors_)

        # self.cm_ = pg.colormap.get(self.list_cmpas[43])
        # self.cm_ = generatePgColormap("cividis")
        # self.spec_item.setLookupTable(self.cm_.getLookupTable())
        self.spec_item.setColorMap(self.cm_)
        self.spec_item.setLevels([0, 1])
        self.plot.hideAxis("bottom")
        self.plot.hideAxis("left")
        self.ui.graphSpectral.setLayout(self.layout_spec)

        self.view.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        # self.cmap_t = QtCore.QTimer()
        # self.cmap_t.timeout.connect(self.update_cmap)
        # self.cmap_t.start(2500)
        # self.cmap_cnt = 0


    def update_cmap(self):
        self.cmap_cnt += 1
        print(self.cmap_cnt)
        self.cm_ = pg.colormap.get(self.list_cmpas[self.cmap_cnt])
        self.spec_item.setLookupTable(self.cm_.getLookupTable())
        self.spec_item.setLevels([0, 1])

    def init_plots(self):
        self.nbr_channels = 1
        self.init_biosignal_plot()
        self.init_biosignal_thumbnail_plot()
        self.init_audio_plot()
        self.init_sound_plot()
        self.init_spectogram_plot()
    
    def reset_plots(self):
        self.graphWidget_biosig.clear()
        self.graphWidget_sound.clear()

        # restart the graph so that a new motion instance is created and the last one is forgot
        self.x = np.zeros(1000)
        self.y = np.zeros(1000)
        colors = ["dodgerblue", "k", "orange", "mediumseagreen", "dodgerblue", "slateblue", "violet"]
        
        self.curves_biosig = [pg.PlotCurveItem(x=self.x, y=self.y, autoDownsample=True, antialias=True,
                                               pen=pg.mkPen(colors[0], width=2)) for i in range(self.nbr_channels)]
        
        self.curves_audio = [pg.PlotCurveItem(x=self.x, y=self.y, autoDownsample=True, antialias=True,
                                        pen=pg.mkPen(colors[0], width=2)) for i in range(self.nbr_channels)]

        for i, curve in enumerate(self.curves_audio):
            self.graphWidget_sound.addItem(curve)

        for i, curve in enumerate(self.curves_biosig):
            self.graphWidget_biosig.addItem(curve)

    def init_streams(self):
        self.update_buffer_interval = 10 #ms between buffer updates
        self.update_spectrum_interval = int(self.image_frame_update*1000) #ms between screen updates
        self.update_signals_interval = int(self.signal_frame_update*1000) #ms between screen updates
        # self.update_fft_interval = 100 #ms

        #update graph timer
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_graph_biosig)
        self.update_timer.start(self.update_signals_interval)

        #update buffer timer
        self.update_buffer_timer = QtCore.QTimer()
        self.update_buffer_timer.timeout.connect(self.update_buffer)
        self.update_buffer_timer.start(self.update_buffer_interval)

    def close_streams(self):
        self.update_timer.stop()
        self.update_buffer_timer.stop()

    def update_buffer(self):
        x = np.frombuffer(self.biosignals.shared_index, dtype=np.float64)
        y = np.frombuffer(self.biosignals.shared_values, dtype=np.float64)

        pos = np.argmin(abs(self.x_plot - x[0]))
        delay = self.buffer_size-(self.signal_plot_size-pos)

        if(delay > 0):
            self.x_plot[:-delay] = self.x_plot[delay:]
            self.x_plot[pos-delay:] = x
            self.y_plot[:-delay] = self.y_plot[delay:]
            self.y_plot[pos-delay:] = y
        elif(delay < 0):
            # print("data was lost")
            self.x_plot[:-delay] = self.x_plot[delay:]
            self.x_plot[-self.buffer_size:] = x
            self.y_plot[:-delay] = self.y_plot[delay:]
            self.y_plot[-self.buffer_size:] = y
        else:
            pass

    def update_graph_biosig(self):
        #update biosig
        # self.graphWidget_biosig.setXRange(min(self.x_plot[self.x_plot>0])/self.sr, max(self.x_plot)/self.sr)
        self.graphWidget_biosig.setXRange(0, self.plot_duration)
        self.curves_biosig[0].setData(np.linspace(0, self.plot_duration, int(self.plot_duration*self.sr)), self.y_plot)
        #update thumbnail
        self.graphWidget_biosig_thumb.setXRange(0, 1)
        self.curves_biosig_thumb[0].setData(np.linspace(0, 1, int(1*self.sr)), self.y_plot[-int(1*self.sr):])

        #update sound
        freq_buffer = np.frombuffer(self.sound.shared_freq_buffer, dtype=np.float64)
        audio_buffer = np.frombuffer(self.sound.shared_audio_buffer, dtype=np.float64)
        self.graphWidget_soundwave.setXRange(0, self.plot_duration)
        self.curves_audiowave[0].setData(np.linspace(0, self.plot_duration, len(audio_buffer)), audio_buffer)

        self.graphWidget_sound.setXRange(0, 44100//4)
        self.curves_audio[0].setData(np.linspace(0, 44100//2, len(freq_buffer)), freq_buffer)
        # print(max(freq_buffer))

        #update image
        image = np.frombuffer(self.sound.shared_spec_buffer, dtype=np.float64)
        image = image/(1+np.max(image))
        img_reshaped = image.reshape((self.num_image_frames, 500))
        # print(np.shape(img_reshaped))
        self.spec_item.setImage(img_reshaped[:, :500//2])

    def configureAcquisition(self):
        self.sr = int(self.intro_ui.textEdit_sampling_rate.toPlainText())
        self.mac = self.intro_ui.textEdit_mac_address.toPlainText()
        self.signal = [self.intro_ui.textEdit_signalType.toPlainText()]
        self.buffer_size = int(self.intro_ui.textEdit_buffer_size.toPlainText())
        # self.buffer_size = 68 #TODO: check if needs to be added as a configuring parameter

        self.n_i = 0

    def LaunchAcquisition(self):
        self.configureAcquisition()
        self.configurePlots()

        self.LaunchBiosignals()

        print("Launching Bioplux Process")
        #wait for biosignals connectiom
        while self.biosignals.plux_connected.value == 0:
            time.sleep(1) #wait connection

        print("Launching Sound Process")
        self.LaunchSound()
        while self.sound.sound_connected.value == 0:
            time.sleep(1) #wait connection

        #launch plots
        self.init_streams()

    def StopAcquisition(self):
        self.updateButtonsStatesStop()
        #stop timers
        self.close_streams()
        # reset plots
        self.reset_plots()
        #close biosignals
        self.biosignals.terminate_biosignal()
        #close sound
        self.sound.terminate_sound()
        #update cntr
        self.launch_cntr += 1

        #close sound
        # self.window().close()

    def LaunchBiosignals(self):
        self.biosignals = Biosignals(self.mac, self.sr, self.buffer_size, self.signal)
        self.biosignals.launch_biosignals()

    def LaunchSound(self):
        self.sound = Sound(self.plot_duration, self.image_frame_update, self.num_image_frames, self.biosignals.shared_values)
        # self.sound = Sound(self.plot_duration, self.frame_update, self.num_frames)
        self.sound.launch_sound(self.current_example_id)


    # def start(self):





    # def launch_app(self):
    #     """
    #     source: launch app for streaming OpenSignals Data
    #     """
    #     process = mp.Process(
    #         name='biosoundscape_app',
    #         target=self.run,
    #     )
    #     process.start()


# Loading screen
class LoadScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_LoadingScreen()
        self.ui.setupUi(self)

        ## UI ==> INTERFACE CODES
        ########################################################################

        ## PushButtons to Launch
        self.updateButtonsStatesLaunch()
        self.readExamples()
        self.ui.pushButton_Launch.clicked.connect(self.LaunchMW)
        self.ui.comboBox_examples.currentIndexChanged.connect(self.comboBoxExamplesChange)
        # self.ui.comboBox_signalType.currentIndexChanged.connect(self.comboBoxSignalChange)

        # CHANGE DESCRIPTION

        # Initial Text
        # self.ui.label_description.setText("<strong>WELCOME</strong> TO MY APPLICATION")

        # Change Texts
        # QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        # QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    def readExamples(self):
        with open('example_config.json', 'r') as file:
            # Load the JSON data
            self.examples = json.load(file)

        self.updateConfiguration()

    def updateConfiguration(self):
        example_text = self.ui.comboBox_examples.currentText()
        self.example_ind = example_text.split()[1]
        self.current_example_id = "experience" + self.example_ind
        self.current_example = self.examples[self.current_example_id]
        self.ui.textEdit_buffer_size.setTextColor("gray")
        self.ui.textEdit_sampling_rate.setTextColor("gray")
        self.ui.textEdit_signalType.setTextColor("gray")
        self.ui.textEdit_mac_address.setTextColor("gray")

        self.ui.textEdit_mac_address.setText(self.current_example["mac"])
        self.ui.textEdit_sampling_rate.setText(str(self.current_example["sr"]))
        self.ui.textEdit_buffer_size.setText(str(self.current_example["buffer_size"]))
        # signal_index = self.ui.comboBox_signalType.findText(self.current_example["signal"])
        # self.ui.comboBox_signalType.setCurrentIndex(signal_index)
        self.ui.textEdit_signalType.setText(str(self.current_example["signal"]))

    # def comboBoxSignalChange(self, index):
    #     self.signal = [self.ui.comboBox_signalType.currentText()]

    def comboBoxExamplesChange(self, index):
        example_text = self.ui.comboBox_examples.currentText()
        self.example_ind = example_text.split()[1]
        self.updateConfiguration()

    def updateButtonsStatesLaunch(self):
        self.ui.pushButton_Stop.setEnabled(True)
        # self.ui.pushButton_Launch.setDisabled(True)
        # self.ui.comboBox_examples.setDisabled(True)


    ## ==> APP FUNCTIONS
    ########################################################################
    def LaunchMW(self):
        #update button states
        self.updateButtonsStatesLaunch()
        #Launch Main Window with plots
        # SHOW MAIN WINDOW
        self.main = MainWindow(self.ui, self.current_example_id)
        self.main.show()
        # CLOSE SPLASH SCREEN
        # self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('styles/plot_styles.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
    window = LoadScreen()
    sys.exit(app.exec_())


    #TODO:
    #include mini-plots with 1 second thumbnail
    #make experiences setup work
    #include audio signal
    #include window of theme
    #include story of Hui
    #prepare slides
    #prepare the signal acquisition with EDA and Force
    #are there other variations?
    #do the peak detection with ECG
    #do the derivative of the envelope in the EMG, just to check it out


