#!/usr/bin/env python3

import configparser
import time
import rtmidi

from CK_rec.setup import Setup
from CK_rec.rec_classes import CK_rec

#get config
config = configparser.ConfigParser()
config.read("midirecorder_settings.ini")
if (not config.has_section("midi_settings")):
    config.add_section('midi_settings')
if (not config.has_section("outfile_settings")):
    config.add_section("outfile_settings")
if (not config.has_section("recorder_settings")):
    config.add_section("recorder_settings")
if (not config.has_section("display_settings")):
    config.add_section("display_settings")
midi_settings = config["midi_settings"]
outfile_settings = config["outfile_settings"]
recorder_settings = config["recorder_settings"]
display_settings = config["display_settings"]

debug = recorder_settings.getboolean("debug", False)
display_note_on_symbol = display_settings.get("note_on_symbol", "x")
display_note_off_symbol = display_settings.get("note_off_symbol", " ")

# Start the Device
codeK = Setup()
codeK.print_welcome()
try:
    myPort = int(midi_settings.get("port"))
except (KeyError, TypeError) as e:
    myPort = codeK.perform_setup()

codeK.open_port(myPort)

try:
    on_id = int(midi_settings.get("device_id"))
except (KeyError, TypeError) as e:
    on_id = codeK.get_device_id()

print("your note on id is: ", on_id)

# record
midiRec = CK_rec(myPort, \
                 on_id, \
                 display_note_on_symbol = display_note_on_symbol, \
                 display_note_off_symbol=display_note_off_symbol, \
                 debug=debug)
codeK.set_callback(midiRec)

# Loop to program to keep listening for midi input
try:
    while True:
        time.sleep(0.001)
        #only update the screen every 100 cycles
        if i >= 100:
            midiRec.update_display()
            i = -1
        i += 1
except KeyboardInterrupt:
    midiRec.print_display_footer()
    print("")
finally:
    try:
        name = outfile_settings.get("filename")
    except (KeyError, TypeError) as e:
        name = input('\nsave midi recording as? " \
                    +"(leaving the name blank discards the recording): ')
    if (name != ""):
        midiRec.saveTrack(name)
    codeK.end()
