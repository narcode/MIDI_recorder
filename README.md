# Simple MIDI Recorder
 :notes: MIDI recorder tool. Record and save a stream of midi input as a midi file.
 It also provides you with a nice visual output of the midi signals coming in.

###### (Developed as a support tool for the [CodeKlavier](https://codeklavier.space))

## installation instructions

- make sure you have python3 installed
- pip3 install python-rtmidi
- pip3 install mido

Or use pip3 to install the dependencies with ``pip3 install -r requirements.txt``.

## recording the midi input

Run the python code via:

``python3 recorder.py`` or ``./recorder.py``

## using your own settings

The midi recoder loads the setrings from the ``midirecorder_settings.ini`` file.
You can edit this file according to your needs. There are four sections with
settings you can adjust: 'recorder', 'midi_settings', 'outfile_settings', and 
'display_settings'.

### Recorder

This section provides settings for the recoder script itself. Enable debugging
if you are interested in more information on the proces. The debug will screw
up the nice display though.

### midi_settings

You can enter the midi port and the device_id in the settings file, so you
don't have to enter it every time you use the same device. This section is
optional: if you leave it out, the script will ask you for these settings.

### outfile_settings

You can specify the filename of the recoding. This section is optional. If you
leave it out: the program will ask you for a filename. If you leave it out: no
recording is saved.

### display_settings

Adjust the speed the display updates. Enter the symbols for note_on and note_off that you want to use for displaying
your recording on the screen. This section is optional. Defaults are 'x' en ' '
(space).

# Support

CodeKlavier is developed thanks to the support of **Stimuleringsfonds Creatieve Industrie**
