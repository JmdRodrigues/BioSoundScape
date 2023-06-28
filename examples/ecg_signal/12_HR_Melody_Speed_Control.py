import time

from pyo import *

# Try to import MidiFile from the mido module. You can install mido with pip:
#   pip install mido

try:
    from mido import MidiFile
    import mido
except:
    print("The `mido` module must be installed to run this example!")
    exit()

# Opening the MIDI file...
mid_file = MidiFile("../../data/music/pachelbel-canon-in-d-major.mid")

s = Server().boot().start()
# A little audio synth to play the MIDI events.
mid = Notein()
amp = MidiAdsr(mid["velocity"])
pit = MToF(mid["pitch"])
osc = Osc(SquareTable(), freq=pit, mul=amp)
osc.mix(1)
rev = STRev(osc, revtime=1, cutoff=4000, bal=0.2).out()

# Let's try using a trigger
met = Metro().play()
c = Counter(met)
d = mido.merge_tracks(mid_file.tracks)

messages = []
for i in d:
    if(i.is_meta):
        pass
    else:
        messages.append(i)

def play_tune():
    message = messages[int(c.get())].bytes()
    print(message)
    # if(message[0]<159 and message[0]>144):
    #     s.makenote(pitch=int(message[1]), velocity=int(message[2]), duration=1)
    # s.addMidiEvent(*message)


t = TrigFunc(met, play_tune)
# s.gui(locals())

# ... and reading its content.
for m in messages:
    time.sleep(0.5)
    # m = messages[int(c.get())]
    # For each message, we convert it to integer data with the bytes()
    # method and send the values to pyo's Server with the addMidiEvent()
    # method. This method programmatically adds a MIDI message to the
    # server's internal MIDI event buffer.
    s.addMidiEvent(*m.bytes())