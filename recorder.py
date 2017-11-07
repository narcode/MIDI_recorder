import time
import rtmidi

from CK_rec.setup import Setup
from CK_rec.rec_classes import CK_rec

# Start the Device
codeK = Setup()
myPort = codeK.perform_setup()
codeK.open_port(myPort)
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
    name = input("\nsave midi recording as? : ")
    if (name != ""):
        midiRec.saveTrack(name)
    codeK.end()
