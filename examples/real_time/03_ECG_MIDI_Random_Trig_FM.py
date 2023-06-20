from tools.sonification import BioSound
import time

sonify = BioSound(example="example3", signal=["ECG"])
sonify.setup()
sonify.start()