from tools.sonification import BioSound

sonify = BioSound(example="example5", signal=["EMG"], n_frames=1024)
sonify.setup()
sonify.start()