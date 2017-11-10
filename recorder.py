#!/usr/bin/env python3

import configparser
import time
import rtmidi

from CK_rec.setup import Setup
from CK_rec.rec_classes import CK_rec

#get config
config = configparser.ConfigParser()
config.read("midirecorder_settings.ini")
try:
    midi_settings = config["midi_settings"]
except KeyError:
    print("No midi settings in ini file.")
    midi_settings = {}
try:
    outfile_settings = config["outfile_settings"]
except KeyError:
    print("No outfile settings in ini file.")
    outfile_settings = {}

# Start the Device
codeK = Setup()
codeK.print_welcome()
try:
    myPort = int(midi_settings.get("port"))
except KeyError:
    myPort = codeK.perform_setup()

codeK.open_port(myPort)

try:
    on_id = int(midi_settings.get("device_id"))
except KeyError:
    on_id = codeK.get_device_id()

print("your note on id is: ", on_id)

# record
midiRec = CK_rec(myPort, on_id)
codeK.set_callback(midiRec)

# Loop to program to keep listening for midi input
try:
    while True:
        time.sleep(0.001)
except KeyboardInterrupt:
    print("")
finally:
    try:
        name = outfile_settings.get("filename")
    except KeyError:
        name = input("\nsave midi recording as? : ")
    if (name != ""):
        midiRec.saveTrack(name)
    codeK.end()
