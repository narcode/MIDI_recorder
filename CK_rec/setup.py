import time
import rtmidi

class Setup:
    """Helper class to perform some basic setup.
    """

    def __init__(self):
        """Initialise the class and set variables.
        """
        self._midiin = rtmidi.MidiIn()
        self._midiout = rtmidi.MidiOut()
        self._ports = self._midiin.get_ports()
        self._ports_out = self._midiout.get_ports()

    def print_welcome(self):
        """Prints welcome message
        """

        print("");
        for i in range(1, 6):
            string = "####"
            space = " ";
            if i == 1:
                print(string[:4] + space + string[:1] + space*2 + string[:1] \
                      + space*4 + string[:4] + space + string[:4] + space \
                      + string[:4])
            elif i == 2:
                print(string[:1] + space*4 + string[:1] + space + string[:1] \
                      + space*5 + string[:1] + space*2 + string[:1] + space \
                      + string[:1] + space*4 + string[:1])
            elif i == 3:
                print(string[:1] + space*4 + string[:2]+ space*6 + string[:4] \
                      + space + string[:4] + space + string[:1])
            elif i == 4:
                print(string[:1] + space*4 + string[:1] + space + string[:1] \
                      + space*5 + string[:1] + space + string[:1] + space*2 \
                      + string[:1] + space*4 + string[:1])
            elif i == 5:
                print(string[:4] + space + string[:1] + space*2 + string[:1] \
                      + space*4 + string[:1] + space*2 + string[:1] + space \
                      + string[:4] + space + string[:4])
            time.sleep(0.2)

        print("\nWelcome to the Codeklavier MIDI Recorder!\n")

    def show_ports(self):
        """Prints the available midi ports.
        """
        print("These are your detected MIDI devices:", "\n")
        for port in self._ports:
            print(self._ports.index(port), " -> ", port)

    def get_port_from_user(self):
        """Lets the user select a midi port available on the system.
        
        Loops until the user selects a valid port or exits the program.
        
        :return: the selected midiport by the user
        :rtype: int
        """
        selected_midiport = -1
        while selected_midiport < 0:
            try:
                choice = input("Please choose the MIDI device (number) you " \
                               + "want to use and hit Enter:")
                selected_midiport = int(choice)
                if (selected_midiport < 0
                        or selected_midiport >= len(self._ports)):
                    print("Invalid number, please try again:")
                    selected_midiport = -1
                else:
                    return selected_midiport
            except KeyboardInterrupt:
                print("\n", "You want to quit? ¯\('…')/¯  ok, Bye bye.")
                exit()
            except ValueError:
                print("Sorry, type a valid port numer!")

    def open_port(self, pnum):
        """Open the midi port for recording.

        :param int pnum: the port number
        "raises Exception: if there are no midiports"
        """
        print("You have chosen: ", self._ports[pnum])

        if self._ports:
            #TODO: do we need to check on the existence of ports?
            self._midiin.open_port(pnum)
            # ignore sysex, timing and active sense messages
            self._midiin.ignore_types(True, True, False)
        else:
            raise Exception("No midi ports! Maybe open a virtual device?")

    def open_port_out(self, num):
        """Open the midi output port

        :param int num: the midi port number
        """
        print("opened midi out port")

        if self._ports_out:
            self._midiout.open_port(num)

    def close_port(self):
        """Close the midi ports.
        """
        self._midiin.close_port()
        #TODO: add close out port too

    def get_message(self):
        """Get the midi in message

        :return: the midi message
        """
        return self._midiin.get_message()

    def send_message(self, message):
        """Send a midi message to the out port.
        
        :param message: the message to send
        :return: something
        """
        return self._midiout.send_message(message)

    def set_callback(self,cb):
        """Set the callback on the midi in.

        :param cb: the callback to call
        """
        self._midiin.set_callback(cb)

    def get_device_id(self):
        """Gets the user to send a midi signal te determine the device id.

        :return: the device id
        :rtype: int
        """
        print("Hit any note to get the device_id.")
        while True:
            msg = self.get_message()
            if msg:
                message, deltatime = msg
                if message[0] != 254: #active sense ignore
                    device_id = message[0]
                    if device_id:
                        return device_id

    def perform_setup(self):
        """Perform the setup

        Get the user to select a midi input port.

        :return: the selected midi input port
        :rtype: int
        """
        self.show_ports()
        myPort = self.get_port_from_user()
        return myPort

    def end(self):
        """Close ports and clean up

        TODO: change to __del__ ??
        """
        print("Bye bye from CodeKlavier Recorder! see you next time 🎹\n")
        self.close_port()
        del self._midiin

def main():
    codeK = Setup()
    my_midiport = codeK.perform_setup()
    codeK.open_port(my_midiport)

    if my_midiport >= 0:
        print("CodeKlavier is ON. Showing incoming MIDI messages. " \
              + "Press Control-C to exit.")
        try:
            timer = time.time()
            while True:
                msg = codeK.get_message()

                if msg:
                    message, deltatime = msg
                    print("deltatime: ", deltatime, "msg: ", message)

                time.sleep(0.01)

        except KeyboardInterrupt:
            print("")
        finally:
            codeK.end()

if __name__ == "__main__":
    main()
