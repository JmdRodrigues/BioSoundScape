from tools.sonification import BioSound
import time

sonify = BioSound(example="example2", signal=["EMG"])
sonify.setup()
sonify.start()