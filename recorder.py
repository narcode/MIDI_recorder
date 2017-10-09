import time
import rtmidi
import mido
from mido import Message, MidiFile, MidiTrack

#import from parrentdir
import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from CK_rec.setup import Setup

#mode
debug = True

# Start the Device
codeK = Setup()
myPort = codeK.perform_setup()
codeK.open_port(myPort)
on_id = codeK.get_device_id()
print('your note on id is: ', on_id, '\n')


# Start the recorder
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# record
class CK_rec(object):
    def __init__(self, port):
        self.port = port

    def __call__(self, event, data=None):
        message, deltatime = event
        if message:
            miditime = int(round(mido.second2tick(deltatime, mid.ticks_per_beat, mido.bpm2tempo(120))))
            if debug:
                print('deltatime: ', deltatime, 'msg: ', message)
            if message[0] == on_id:
                track.append(Message('note_on', note=message[1], velocity=message[2], time=miditime))
            else:
                # print("note off!")
                track.append(Message('note_off', note=message[1], velocity=message[2], time=miditime))


print("\nCodeKlavier is ready and ON.")
print("You are now RECORDING")
print("\nPress Control-C to exit.")

codeK.set_callback(CK_rec(myPort))

# Loop to program to keep listening for midi input
try:
    while True:
        time.sleep(0.001)
except KeyboardInterrupt:
    print('')
finally:
    name = input('save midi recording as: ')
    mid.save('recordings/'+name+'.mid')
    codeK.end()
