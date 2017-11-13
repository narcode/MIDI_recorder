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
if (not config.has_section("recorder")):
    config.add_section("recorder")
if (not config.has_section("display_settings")):
    config.add_section("display_settings")
midi_settings = config["midi_settings"]
outfile_settings = config["outfile_settings"]
recorder_settings = config["recorder"]
display_settings = config["display_settings"]

display_speed_options = {
    "fastest": 15,
    "faster": 30,
    "fast": 45,
    "medium": 60,
    "slow": 75,
    "slower": 90,
    "slowest": 105}

debug = recorder_settings.getboolean("debug", False)
display_note_on_symbol = display_settings.get("note_on_symbol", "x")
display_note_off_symbol = display_settings.get("note_off_symbol", " ")
display_speed = display_speed_options.get(
    display_settings.get("speed", "medium"))

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
    i = 0
    while True:
        time.sleep(0.001)
        if i >= display_speed:
            midiRec.update_display()
            i = -1
        i += 1
except KeyboardInterrupt:
    print("")
    midiRec.print_display_footer()
finally:
    try:
        name = outfile_settings.get("filename")
    except (KeyError, TypeError) as e:
        name = input('\nsave midi recording as? " \
                    +"(leaving the name blank discards the recording): ')
    if (name != ""):
        midiRec.saveTrack(name)
    codeK.end()
