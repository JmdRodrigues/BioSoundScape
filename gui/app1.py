import random

from pyo import *

import pyqtgraph as pg
import sys

import numpy as np
import time

import multiprocessing as mp

from tools.plux_device import In_BiosignalsPlux
from tools.sonification import SoundGenerator

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QMainWindow, QLabel
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QColor, QPixmap, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class SoundWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, plot_duration, spectrum_update, x_plot):
        super().__init__()
        self.plot_duration = 1.5
        self.spectrum_update = spectrum_update
        self.x_index = x_plot

    def run(self):
        self.sound = SoundGenerator("example2", self.plot_duration, self.spectrum_update, self.x_index)
        self.sound.start()
        self.sound_check = 1
        while True:
            pass

# class UpdateBuffer(QThread):

uiclass, baseclass = pg.Qt.loadUiType("biosoundscape_gui.ui")

class MainWindow(uiclass, baseclass):
    def __init__(self, x_data, y_data, fs, plot_duration):
        super(MainWindow, self).__init__()
        self.x_data = x_data
        self.y_data = y_data

        self.fs = fs
        self.plot_duration = plot_duration
        self.plot_size = int(self.plot_duration * self.fs)

        self.x_plot = np.zeros(self.plot_size)
        self.y_plot = np.zeros(self.plot_size)

        # self.x_audio = np.zeros(10*fs)
        # self.y_audio = np.zeros(10*fs)

        self.cntr = 0
        # self.x_data = np.linspace(0, 255, 256)
        # self.y_data = np.random.random(256)

        self.spectrum_update = 0.015
        self.signals_update = 0.015

        self.setupUi(self)

        #init plots
        print("Launching Pyo")
        self.sound_connected = 0
        self.launchSoundThread()
        while True:
            try:
                self.worker.sound_check
                break
            except:
                time.sleep(1)
                pass
        print("Configuring Plots")
        self.plots()
        print("Initiating Streams")
        self.init_streams()
        # self.init_audio_generator()

    def plots(self):
        self.nbr_channels = 1
        self.init_biosignal_plot()
        self.init_sound_plot()
        self.init_spectogram_plot()

    def launchSoundThread(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = SoundWorker(self.plot_duration, self.spectrum_update, self.x_plot)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()
        self.sound_connected = 1

    def init_biosignal_plot(self):
        # Create the pyqtgraph window
        self.layout_biosig = QGridLayout()
        self.graphWidget_biosig = pg.PlotWidget()
        self.layout_biosig.addWidget(self.graphWidget_biosig)
        self.graphWidget_biosig.plot()
        self.graphWidget_biosig.enableAutoRange(x=False, y=True)
        self.graphWidget_biosig.showGrid(x=True, y=False, alpha=0.3)
        self.graphWidget_biosig.setXRange(0, 10*self.fs)
        # self.graphWidget_biosig
        self.graphWidget_biosig.setBackground("floralwhite")
        self.graphWidget_biosig.setLabel("left", "Amplitude (n.a.)")
        self.graphWidget_biosig.setLabel("bottom", "Time (s)")
        # Set Range
        self.graphWidget_biosig.getPlotItem().hideAxis("bottom")
        self.graphWidget_biosig.getPlotItem().hideAxis("left")
        self.graphBiosignal.setLayout(self.layout_biosig)

        self.graphWidget_biosig.clear()
        # restart the graph so that a new motion instance is created and the last one is forgot
        self.x = np.linspace(0, 199, 200)
        self.y = np.random.random(200)
        colors = ["k", "orange", "mediumseagreen", "dodgerblue", "slateblue", "violet"]
        self.curves_biosig = [pg.PlotCurveItem(x=self.x, y=self.y, autoDownsample=True, antialias=True,
                                                pen=pg.mkPen(colors[i], width=2)) for i in range(self.nbr_channels)]

        for i, curve in enumerate(self.curves_biosig):
            self.graphWidget_biosig.addItem(curve)

    def init_sound_plot(self):
        # Create the pyqtgraph window
        self.layout_sound = QGridLayout()
        self.graphWidget_sound = pg.PlotWidget()
        self.layout_sound.addWidget(self.graphWidget_sound)
        self.graphWidget_sound.plot()
        self.graphWidget_sound.enableAutoRange(x=False, y=True)
        self.graphWidget_sound.showGrid(x=True, y=False, alpha=0.2)
        self.graphWidget_sound.setBackground("floralwhite")
        self.graphSound.setLayout(self.layout_sound)

        self.graphWidget_sound.clear()
        # restart the graph so that a new motion instance is created and the last one is forgot
        self.x = np.linspace(0, 199, 200)
        self.y = np.random.random(200)
        colors = ["k", "orange", "mediumseagreen", "dodgerblue", "slateblue", "violet"]
        self.curves_audio = [pg.PlotCurveItem(x=self.x, y=self.y, autoDownsample=True, antialias=True,
                                              pen=pg.mkPen(colors[i], width=2)) for i in range(self.nbr_channels)]

        for i, curve in enumerate(self.curves_audio):
            self.graphWidget_sound.addItem(curve)

    def init_spectogram_plot(self):
        # Create the pyqtgraph window
        self.layout_spec = QGridLayout()
        self.view = pg.GraphicsLayoutWidget()
        self.layout_spec.addWidget(self.view)
        self.plot = self.view.addPlot()
        self.spec_item = pg.ImageItem()
        self.plot.addItem(self.spec_item)
        # self.layout_spec.addWidget(self.graphWidget_spec)
        self.plot.hideAxis("bottom")
        self.plot.hideAxis("left")
        self.graphSpectral.setLayout(self.layout_spec)


    def init_streams(self):
        # initial methods for
        self.buffer_size = len(self.x_data)
        self.buffer_duration = int(self.buffer_size/self.fs) #in seconds
        self.update_buffer_interval = 10 #ms between buffer updates
        self.update_spectrum_interval = int(self.spectrum_update*1000) #ms between screen updates
        self.update_signals_interval = int(self.signals_update*1000) #ms between screen updates
        # self.update_fft_interval = 100 #ms

        #update graph timer
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_graph_biosig)
        self.update_timer.start(self.update_signals_interval)

        # # update graph timer
        # self.update_timer2 = QtCore.QTimer()
        # self.update_timer2.timeout.connect(self.update_graph_sound)
        # self.update_timer2.start(self.update_interval)

        # update graph timer
        # self.update_timer3 = QtCore.QTimer()
        # self.update_timer3.timeout.connect(self.update_spec_image)
        # self.update_timer3.start(self.update_spectrum_interval)

        #update buffer timer
        self.update_buffer_timer = QtCore.QTimer()
        self.update_buffer_timer.timeout.connect(self.update_buffer)
        self.update_buffer_timer.start(self.update_buffer_interval)

        #modulate audio signal
        self.modulateAudio_timer = QtCore.QTimer()
        self.modulateAudio_timer.timeout.connect(self.audioModulator)
        self.modulateAudio_timer.start(self.update_buffer_interval)

        # # compute audio processing
        # self.audioProcessing_timer = QtCore.QTimer()
        # self.audioProcessing_timer.timeout.connect(self.audioProcessing)
        # self.audioProcessing_timer.start(self.update_buffer_interval)

    def audioModulator(self):
        """Modulate Audio"""
        # print("modulating...")
        # self.sound.b.setInput(Sig(float(np.mean(np.abs(self.y_data)))))
        self.worker.sound.fm.setIndex(float(np.std(np.abs(self.y_data))))
        # self.worker.sound.sine.setFreq(440+float(np.sum(np.abs(self.y_data))))

        # val = self.sound.s.getCurrentTimeInSamples()

        # self.x_audio[self.cntr] = val
        # self.y_audio[self.cntr] = self.sound.s.getCurrentAmp()[0]# self.x_audio[]
        # print(self.x_audio[0])
        # if(self.cntr == len(self.x_audio)-1):
        #     self.cntr = 0
        # else:
        #     self.cntr += 1


    # def audioProcessing(self):


    def update_buffer(self):
        x = np.frombuffer(self.x_data, dtype=np.float64)
        y = np.frombuffer(self.y_data, dtype=np.float64)

        pos = np.argmin(abs(self.x_plot - x[0]))
        delay = self.buffer_size-(self.plot_size-pos)

        if(delay > 0):
            self.x_plot[:-delay] = self.x_plot[delay:]
            self.x_plot[-self.buffer_size:] = x
            self.y_plot[:-delay] = self.y_plot[delay:]
            self.y_plot[-self.buffer_size:] = y
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
        self.graphWidget_biosig.setXRange(self.x_plot[0], self.x_plot[-1])
        self.curves_biosig[0].setData(self.x_plot[::4], self.y_plot[::4])
        #update sound
        self.graphWidget_sound.setXRange(0, 44100 // 10)
        self.curves_audio[0].setData(np.linspace(0, 44100 // 2, len(self.worker.sound.freq_buffer)),
                                     self.worker.sound.freq_buffer)

        self.spec_item.setImage(self.worker.sound.spec_buffer[:, :])

    # def update_spec_image(self):
        # update image


class APP1():
    def __init__(self, mac, fs, buffer_size, signal):
        self.buffer_size = buffer_size

        self.shared_index = mp.RawArray('d', range(self.buffer_size))
        self.shared_values = mp.RawArray('d', range(self.buffer_size))
        self.plux_connected = mp.RawValue('i', 0)

        self.mac = mac
        self.fs = fs
        self.n_i = 0

        self.signal = signal


    def launch_biosignals(self):
        """
            source: launch app for streaming OpenSignals Data
        """
        process = mp.Process(
            name='biosignalsplux',
            target=self.on_start,
            args=[self.signal]
        )
        process.start()

    def launch_app(self):
        """
        source: launch app for streaming OpenSignals Data
        """
        process = mp.Process(
            name='biosoundscape_app',
            target=self.run,
        )
        process.start()

    def on_start(self, biosig_type):
        self.device = In_BiosignalsPlux(self.mac, freq=self.fs, on_data=self.receive_buffer, signal=biosig_type)
        self.plux_connected.value = 1
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

    def run(self):
        self.app = QApplication(sys.argv)
        self.w = MainWindow(self.shared_index, self.shared_values, self.fs, plot_duration=3)
        # show main window app
        self.w.show()
        #set app style
        with open('style/plot_styles.qss', 'r') as f:
            style = f.read()
            self.app.setStyleSheet(style)

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            sys.exit(self.app.instance().exec_())
        self.app.exec()

if __name__ == "__main__":
    app_1 = APP1(mac="00:07:80:8C:AD:C9", fs=1000, buffer_size=256, signal=["ACC_X"])

    wait_biosig = "launching biosignalsplux..."
    print(wait_biosig)
    app_1.launch_biosignals()
    while not app_1.plux_connected.value:
        time.sleep(1)
    print("biosignals device connected...")

    print("launching app...")
    app_1.launch_app()


"""
TODO:
Make the front GUI, which sets the initial configuration:
Parameters: fs, signal type
Session: Experience to select
(Select 1 experience and it will fill the parameter set)
Buttons: Connect to bioplux, Start Experiment, Start Visualization
"""