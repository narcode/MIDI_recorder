import mido
from mido import Message, MidiFile, MidiTrack

from .display import Display

class CK_rec(object):
    """Class for handling the recording
    
    @port is the midi input port
    @device_id is the id passed for note-on messages (sometimes keyboards pass
               note-off as a different id or as velocity=0)
    @tempo is the bpm tempo for the midi recording *** HAS TO BE SET **
    @debug is for posting messages on console or not
    """

    def __init__(self, \
                 port, \
                 device_id, \
                 display_note_on_symbol='x', \
                 display_note_off_symbol=' ', \
                 tempo=120, \
                 debug=True):
        """Initialise the class and set class variables.

        :param int port: the midi input port numer
        :param int device_id: the midi device id
        :param str display_note_on_symbol: symbol to use for display (note on)
        :param str display_note_off_symbol: symbol to use for display (note off)
        :param int tempo: bmp tempo for midi recording (default: 120)
        :param bool debug: run in debug mode (default: True)
        """
        self.port = port
        self.tempo = tempo
        self.debug = debug
        self.on_id = device_id
        self._mid = MidiFile()
        self._track = MidiTrack()
        self.prepareTrack()
        self._activesense = 0
        self.display = Display(display_note_on_symbol, display_note_off_symbol)

    def prepareTrack(self):
        """Show welcome message and append a trak to the tracklist.
        """
        input("Press [ENTER] to start recording...")
        print("\n**** 📹 You are now RECORDING *****")
        print("(Press Control-C to stop the recording)\n")
        self.display.print_header()
        self._mid.tracks.append(self._track)

    def __call__(self, event, data=None):
        """Deal with calling the midi event.

        :param event: the midi event
        :param data: ? (default: None)
        """
        message, deltatime = event
        self._activesense += deltatime
        if message[0] != 254: #ignore active sense
            miditime = round(mido.second2tick(
                                 self._activesense,
                                 self._mid.ticks_per_beat,
                                 mido.bpm2tempo(self.tempo)))
            if self.debug:
                print("deltatime: {0:.3f}, msg: {1}, activecomp: {2:.3f}"\
                    .format(deltatime, message, self._activesense))

            if message[0] == self.on_id:
                self._track.append(Message(
                            "note_on",
                            note=message[1],
                            velocity=message[2],
                            time=miditime))
                self._activesense = 0
                self.display.note_on(message[1])
            elif message[0] == 176:
                self._track.append(Message(
                            "control_change",
                            channel=1,
                            control=message[1],
                            value=message[2],
                            time=miditime))
            else:
                self._track.append(Message(
                            "note_off",
                            note=message[1],
                            velocity=message[2],
                            time=miditime))
                self._activesense = 0
                self.display.note_off(message[1])

    def print_active_notes(self):
        """Use the display to print the active notes.
        """
        self.display.print_line()

    def print_display_footer(self):
        """Print the footer of the display.
        """
        self.display.print_footer()

    def saveTrack(self, name):
        """Save the recording as a midi track (.mid file extension)

        :param str name: filename to save the track to
        """
        self._mid.save("Recordings/" + name + ".mid")
        print("\nRecording saved as: Recordings/" + name + ".mid\n")
