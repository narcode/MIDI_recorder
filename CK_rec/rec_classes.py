import mido
from mido import Message, MidiFile, MidiTrack

# Class for handling the recording
class CK_rec(object):
    def __init__(self, port):
        self.port = port
        self.__mid = MidiFile()
        self.__track = MidiTrack()

    def prepareTrack(self):
        print("\nCodeKlavier is ready and ON.")
        input("Press enter to start recording")
        print("You are now RECORDING")
        print("\nPress Control-C to stop the recording.")
        self.__mid.tracks.append(self.__track)

    def __call__(self, event,tempo, data=None):
        self.prepareTrack()
        message, deltatime = event
        if message:
            miditime = int(round(mido.second2tick(deltatime, mid.ticks_per_beat, mido.bpm2tempo(tempo))))
            if debug:
                print('deltatime: ', deltatime, 'msg: ', message)
            if message[0] == on_id:
                self.__track.append(Message('note_on', note=message[1], velocity=message[2], time=miditime))
            else:
                # print("note off!")
                self.__track.append(Message('note_off', note=message[1], velocity=message[2], time=miditime))

    def saveTrack(self, name):
        mid.save('recordings/'+name+'.mid')
