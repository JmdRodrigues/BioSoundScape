from pyo import *

def genLinSegfromTable(table_, duration):
    t_table = table_.getTable()
    lin_segs = [(duration * i / len(t_table), t_table[i]) for i in range(0, len(t_table))]
    lin_segs.append((1.1, 0))  # fadeoff

    return lin_segs

s = Server()
s.setMidiInputDevice(99)  # Open all input devices.
s.boot()

notes = Notein(scale=1)
t = SndTable("../../data/bioSnds/ecg_mw_key.wav")
lin_segs = genLinSegfromTable(t, 1)
env = MidiLinseg(notes["velocity"], lin_segs)

snd_t = HarmTable([1,0,.33,0,.2,0,.143,0,.111])
a = SineLoop(freq=notes['pitch'], feedback=.1, mul=env).out()
b = SineLoop(freq=notes['pitch']*1.005, feedback=.1, mul=env).out(1)

# notes.keyboard()

s.gui(locals())