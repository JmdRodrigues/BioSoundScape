from pyo import *

s = Server().boot()

t = SndTable("../data/bioSnds/ecg_mw_key.wav")
# Defines tables for the amplitude, the ratio and the modulation index.
amp_table = CosTable([(0, 0), (100, 1), (1024, 0.5), (7000, 0.5), (8192, 0)])
rat_table = ExpTable(
    [(0, 0.5), (1500, 0.5), (2000, 0.25), (3500, 0.25), (4000, 1), (5500, 1), (6000, 0.5), (8192, 0.5),]
)
ind_table = LinTable([(0, 20), (512, 10), (8192, 0)])

# call their graph() method. Use the "yrange" argument to set the minimum
# and maximum bundaries of the graph (defaults to 0 and 1).
frame = t.graphFrame

amp_table.graph(title="Amplitude envelope")
rat_table.graph(title="Ratio envelope")
ind_table.graph(yrange=(0, 20), title="Modulation index envelope")

# Initialize the table readers (TableRead.play() must be called explicitly).
amp = TableRead(table=t, freq=1, loop=False, mul=0.3)
rat = TableRead(table=t, freq=1, loop=False)
ind = TableRead(table=t, freq=1, loop=False)

# Use the signals from the table readers to control an FM synthesis.
fm = FM(carrier=[100, 100], ratio=rat, index=ind, mul=amp).out()

# Call the "note" function to generate an event.
def note(freq=100, dur=1):
    # fm.carrier = [freq, freq * 1.005]
    amp.freq = 1.0 / dur
    rat.freq = 1.0 / dur
    ind.freq = 1.0 / dur
    amp.play()
    # rat.play()
    # ind.play()


# Play one note, carrier = 100 Hz, duration = 2 seconds.
note(440, 2)

s.gui(locals())