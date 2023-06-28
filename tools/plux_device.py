import time
from tools import plux
import numpy as np

def noop (*args, **kwargs):
    pass

class NewDevice(plux.SignalsDev):
    """
    Stub for a Plux based device.
    The onRawFrame should be overwritten
    """

    def __init__(self, address):
        plux.MemoryDev.__init__(address)

        self.onRawFrame = noop

class In_BiosignalsPlux():
    """
    Feeds data frames from a biosiagnal plux based device into the pipeline.

    Examples for biosignal plux devices are: biosignalplux hup and muscleban (for RIoT and Bitalino please have a look at in_riot.py)

    Requires the plux libaray.
    """

    def __init__(self, adr, freq, n_bits=16, on_data=noop, signal=["EMG"]):

        self.adr = adr
        self.freq = freq
        self.n_bits = n_bits
        self.types = [self.identifySensorType(channel_name) for channel_name in signal]
        self.t0 = time.time_ns()
        self.on_data = on_data
        self.device = NewDevice(self.adr)

        print(self.types)
    def identifySensorType(self, name):
        """
        Identify sensor type and define transfer function
        :param name:
        :return:
        """
        if("ACC" in name):
            self.getAccCalibration()
            self.transferFunction = self.accTF
            return "ACC"
        elif("ECG" in name):
            self.transferFunction = self.ecgTF
            return "ECG"
        elif("RESP" in name):
            self.transferFunction = self.respTF
            return "RESP"
        elif("EMG" in name):
            self.transferFunction = self.emgTF
            return "EMG"
        elif("EDA" in name):
            self.transferFunction = self.edaTF
            return "EDA"

    def _set_on_data(self, fn):
        self.on_data = fn

    def _onstop(self):
        self.device.stop()


    def _onstart(self):
        """
        Streams the data and calls frame callbacks for each frame.
        """

        def on_frame_wrap(nSeq, data): #onRawFrame
            nonlocal self
            self.on_data(nSeq, data)

        self.device.onRawFrame = on_frame_wrap

        channel_src = plux.Source()
        channel_src.port = 1  # Number of the port used by this channel.
        channel_src.freqDivisor = 1  # Subsampling factor in relation with the freq, i.e., when this value is
        # equal to 1 then the channel collects data at a sampling rate identical to the freq,
        # otherwise, the effective sampling rate for this channel will be freq / freqDivisor
        channel_src.nBits = self.n_bits  # Resolution in #bits used by this channel.
        channel_src.chMask = 0x01  # Hexadecimal number defining the number of channels streamed by this port, for example:
        # 0x07 ---> 00000111 | Three channels are active.

        self.device.start(self.freq, [channel_src])
        # calls self.device.onRawFrame until it returns True
        self.device.loop()

    def getAccCalibration(self):
        """
        If data is an accelerometer, get calibration values
        """
        calib_file = np.loadtxt("../data/acc_calibration/acc_calibration_0007808CADC9_2023-06-09_10-38-11.txt")
        self.C_X_min = min(calib_file[:, 2]); self.C_X_max = max(calib_file[:, 2])
        C_Y_min = min(calib_file[:, 3]); C_Y_max = max(calib_file[:, 3])
        C_Z_min = min(calib_file[:, 4]); C_Z_max = max(calib_file[:, 4])

    def accTF(self, data):
        """
        transfer function for accelerometer data
        :param data:
        :return:
        """
        return (2*(data - self.C_X_min)/(self.C_X_max-self.C_X_min))-1

    def emgTF(self, data):
        VCC = 3 #in volts
        gain = 1000
        return ((data/(2**self.n_bits))-0.5)*VCC

    def ecgTF(self, data):
        VCC = 3  # in volts
        gain = 1019

        return 1000*(((data / (2 ** self.n_bits)) - 0.5) * VCC) / gain

    def edaTF(self, data):
        VCC = 3  # in volts

        return (((data / (2 ** self.n_bits)) - 0.5) * VCC) / 0.12

    def respTF(self, data):
        VCC = 3
        G_pzt = 1

        return (((data / ((2 ** self.n_bits)-1)) - 0.5) * VCC) / G_pzt

def sampleAcquisition(address="BTH00:07:80:4D:2E:76",
                      duration=20,
                      frequency=1000,
                      code="0x01"):
    """
    Example acquisition.

    Supported channel number codes:
    {1 channel - 0x01, 2 channels - 0x03, 3 channels - 0x07
    4 channels - 0x0F, 5 channels - 0x1F, 6 channels - 0x3F
    7 channels - 0x7F, 8 channels - 0xFF}

    Maximum acquisition frequencies for number of channels:
    1 channel - 8000, 2 channels - 5000, 3 channels - 4000
    4 channels - 3000, 5 channels - 3000, 6 channels - 2000
    7 channels - 2000, 8 channels - 2000
    """

    device = NewDevice(address)
    device.duration = duration
    device.frequency = frequency

    if isinstance(code, str):
        code = int(code, 16)

    device.start(device.frequency, code, 16)
    device.loop()
    device.stop()
    device.close()

if __name__ == "__main__":
    device = In_BiosignalsPlux("00:07:80:8C:AD:C9", freq=50, on_data=print)
    # device = In_BiosignalsPlux("20:16:07:18:15:77", freq=1000, on_data=print)
    # device = In_muscleban("BTH84:FD:27:E5:04:C4", freq=100, on_data=print)
    device._onstart()
    time.sleep(10) # keep open for 10 minutes to debug
    device._onstop()


