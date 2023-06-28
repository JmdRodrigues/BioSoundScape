import sys
import platform
import json
import time
import sched

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
        self.shared_values = mp.RawArray('d', range(self.buffer_size))
        
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
        self.frame_cnt = 0  # initialized frame cnt
        self.shared_spec_buffer = mp.RawArray('d', range(self.num_frames * 512))
        self.shared_freq_buffer = mp.RawArray('d', range(512))

        self.sound_connected = mp.RawValue('i', 0)
        self.shared_modulator = shared_array
    
        # print(self.shared_modulator)

    def run(self, event):
        self.sound = SoundGenerator("example2", self.plot_duration, self.spectrum_update, on_data=self.receive_buffer)
        self.sound.start()
        self.sound_connected.value = 1
        self.init_modulation()
        while not event.is_set():
            pass
        self.stop()
    
    def stop(self):
        self.scheduler.cancel()
        self.sound.stop()

    def receive_buffer(self, indata):
        x, y = zip(*indata[0])
        # print(self.x_index[-1])
        if (self.frame_cnt < self.num_frames):
            self.shared_spec_buffer[self.frame_cnt * 512:self.frame_cnt * 512 + len(y)] = np.abs(np.max(y) - y)
            self.frame_cnt += 1
        else:
            self.shared_spec_buffer[0:-512] = self.shared_spec_buffer[512:]
            self.shared_spec_buffer[-len(y):] = np.abs(np.max(y) - y)
            # self.x_spec_buffer[-1] = self.x_index[-1]
            self.frame_cnt += 1

        self.shared_freq_buffer[:len(y)] = np.abs(np.max(y) - y)

    def init_modulation(self):
        print("init_modulation")
        #modulate audio signal
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.modulation_interval = 10 #in milliseconds
        self.scheduler.enter(self.modulation_interval/1000, 1, self.audioModulator)
        self.scheduler.run()

    def audioModulator(self):
        """Modulate Audio"""
        # print("modulating...")
        self.scheduler.enter(self.modulation_interval/1000, 1, self.audioModulator)
        # self.sound.b.setInput(Sig(float(np.mean(np.abs(self.y_data)))))
        self.sound.fm.setIndex(10*float(np.std(np.abs(self.shared_modulator))))
        self.sound.sine.setFreq(440 + int((100*float(np.mean(np.abs(self.shared_modulator))))**2))
        # self.worker.sound.sine.setFreq(440+float(np.sum(np.abs(self.y_data))))

    def launch_sound(self):
        """
        source: launch app for streaming Audio Data
        """
        self.event = mp.Event()
        self.process = mp.Process(
            name='sound',
            target=self.run,
            args=[self.event]
        )
        self.process.start()

    def terminate_sound(self):
        self.event.set()
        time.sleep(0.25)
        self.process.terminate()
        self.process.join()

# YOUR APPLICATION
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.launch_cntr = 0

        self.ui.pushButton_Launch.clicked.connect(self.LaunchAcquisition)
        self.ui.pushButton_Stop.clicked.connect(self.StopAcquisition)
        self.ui.comboBox_examples.currentIndexChanged.connect(self.comboBoxExamplesChange)
        self.ui.comboBox_signalType.currentIndexChanged.connect(self.comboBoxSignalChange)

        self.readExamples()

    def readExamples(self):
        with open('example_config.json', 'r') as file:
            # Load the JSON data
            self.examples = json.load(file)

        self.updateConfiguration()

    def updateConfiguration(self):
        example_text = self.ui.comboBox_examples.currentText()
        self.example_ind = example_text.split()[1]
        self.current_example = self.examples["example" + self.example_ind]
        self.ui.textEdit_mac_address.setText(self.current_example["mac"])
        self.ui.textEdit_sampling_rate.setText(str(self.current_example["sr"]))
        signal_index = self.ui.comboBox_signalType.findText(self.current_example["signal"])
        self.ui.comboBox_signalType.setCurrentIndex(signal_index)

    def comboBoxSignalChange(self, index):
        self.signal = [self.ui.comboBox_signalType.currentText()]

    def comboBoxExamplesChange(self, index):
        example_text = self.ui.comboBox_examples.currentText()
        self.example_ind = example_text.split()[1]
        self.updateConfiguration()

    def updateButtonsStatesLaunch(self):
        self.ui.pushButton_Stop.setEnabled(True)
        self.ui.pushButton_Launch.setDisabled(True)
        self.ui.comboBox_signalType.setDisabled(True)
        self.ui.comboBox_examples.setDisabled(True)
        self.ui.textEdit_mac_address.setDisabled(True)
        self.ui.textEdit_sampling_rate.setDisabled(True)

    def updateButtonsStatesStop(self):
        self.ui.pushButton_Stop.setEnabled(False)
        self.ui.pushButton_Launch.setDisabled(False)
        self.ui.comboBox_signalType.setDisabled(False)
        self.ui.comboBox_examples.setDisabled(False)
        self.ui.textEdit_mac_address.setDisabled(False)
        self.ui.textEdit_sampling_rate.setDisabled(False)

    def configurePlots(self):
        self.plot_duration = 3 #in seconds
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

    def init_biosignal_plot(self):
        # Create the pyqtgraph window
        self.layout_biosig = QGridLayout()
        self.graphWidget_biosig = pg.PlotWidget()
        self.layout_biosig.addWidget(self.graphWidget_biosig)
        self.graphWidget_biosig.plot()
        self.graphWidget_biosig.enableAutoRange(x=False, y=True)
        self.graphWidget_biosig.showGrid(x=True, y=False, alpha=0.3)
        self.graphWidget_biosig.setXRange(0, 10 * self.sr)
        # self.graphWidget_biosig
        self.graphWidget_biosig.setBackground("floralwhite")
        self.graphWidget_biosig.setLabel("left", "Amplitude (n.a.)")
        self.graphWidget_biosig.setLabel("bottom", "Time (s)")
        # Set Range
        self.graphWidget_biosig.getPlotItem().hideAxis("bottom")
        self.graphWidget_biosig.getPlotItem().hideAxis("left")
        #add to Frame GraphWidget
        self.ui.graphBiosignal.setLayout(self.layout_biosig)

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
        self.ui.graphSound.setLayout(self.layout_sound)

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
        self.ui.graphSpectral.setLayout(self.layout_spec)

    def init_plots(self):
        self.nbr_channels = 1
        self.init_biosignal_plot()
        self.init_sound_plot()
        self.init_spectogram_plot()
    
    def reset_plots(self):
        self.graphWidget_biosig.clear()
        self.graphWidget_sound.clear()

        # restart the graph so that a new motion instance is created and the last one is forgot
        self.x = np.zeros(1000)
        self.y = np.zeros(1000)
        colors = ["k", "orange", "mediumseagreen", "dodgerblue", "slateblue", "violet"]
        
        self.curves_biosig = [pg.PlotCurveItem(x=self.x, y=self.y, autoDownsample=True, antialias=True,
                                               pen=pg.mkPen(colors[i], width=2)) for i in range(self.nbr_channels)]
        
        self.curves_audio = [pg.PlotCurveItem(x=self.x, y=self.y, autoDownsample=True, antialias=True,
                                        pen=pg.mkPen(colors[i], width=2)) for i in range(self.nbr_channels)]

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
        self.curves_biosig[0].setData(self.x_plot[::2], self.y_plot[::2])
        #update sound
        freq_buffer = np.frombuffer(self.sound.shared_freq_buffer, dtype=np.float64)
        self.graphWidget_sound.setXRange(0, 44100 // 10)
        self.curves_audio[0].setData(np.linspace(0, 44100 // 2, len(freq_buffer)), freq_buffer)

        #update image
        self.spec_item.setImage(np.frombuffer(self.sound.shared_spec_buffer, dtype=np.float64).reshape((self.num_image_frames, 512)))

    def configureAcquisition(self):
        self.sr = int(self.ui.textEdit_sampling_rate.toPlainText())
        self.mac = self.ui.textEdit_mac_address.toPlainText()

        self.buffer_size = 256 #TODO: check if needs to be added as a configuring parameter

        self.n_i = 0

    def LaunchAcquisition(self):
        self.updateButtonsStatesLaunch()
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

    def LaunchBiosignals(self):
        self.biosignals = Biosignals(self.mac, self.sr, self.buffer_size, self.signal)
        self.biosignals.launch_biosignals()

    def LaunchSound(self):
        self.sound = Sound(self.plot_duration, self.image_frame_update, self.num_image_frames, self.biosignals.shared_values)
        # self.sound = Sound(self.plot_duration, self.frame_update, self.num_frames)
        self.sound.launch_sound()


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

        ## REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

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

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):
        global counter

        # SET VALUE TO PROGRESS BAR
        # self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 10:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = MainWindow()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open('styles/plot_styles.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
    window = LoadScreen()
    sys.exit(app.exec_())