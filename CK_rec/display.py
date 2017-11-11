class Display:
    """TODO: WRITE DOCSTRING
    """
    
    notes_playing = []
    MAX_MIDI_NOTES = 10 #should be 128 ??
    
    #TODO: move to settings-file?
    NOTE_ON_SYMBOL = "x"
    NOTE_OFF_SYMBOL = " "
    
    def __init__(self):
        """Initialise the class and set variables
        """
        self.notes_playing = [False for x in range(0,self.MAX_MIDI_NOTES)]

    def _check_note_range(self, midinumber):
        """Helper function to check if midinumber is valid
        
        :param int midinumber: the midi not number to check
        :return boolean: True if succesful
        """
        #TODO: is 0 allowed?
        if (midinumber < 0 and midinumber >self.MAX_MIDI_NOTES):
            raise  TypeError("Invalid midi number")
        return True
    
    def note_on(self, midinumber):
        """Register the note with midinumber to on
        
        :param int midinumber: the midinumber of the note being played
        """
        self._check_note_range(midinumber)
        self.notes_playing[midinumber] = True
    
    def note_off(self, midinumber):
        """Register the note with midinumber to off
        
        :param int midinumber: the midinumber of the note not played anymore
        """
        self._check_note_range(midinumber)
        self.notes_playing[midinumber] = False
    
    def print_line(self):
        """Print a single line with the midi notes
        """
        buildstring = [self.NOTE_ON_SYMBOL if x else self.NOTE_OFF_SYMBOL for x in self.notes_playing]
        print("".join(buildstring))

    def print_header(self):
        """Print a header line

        This should help you to navigate between midinumbers
        """
        print("1    5    10   11   15   20   25   30   35   40   45   50   55   60   65   70   75   80   85   90   95   100  105  110  115  120  125  130  135  140  145  150")
        print("|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|____|")

    def print_footer(self):
        """Print a footer line

        This should help you to navigate between midinumbers
        """
        print(" ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ")
        print("|    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |")
        print("1    5    10   11   15   20   25   30   35   40   45   50   55   60   65   70   75   80   85   90   95   100  105  110  115  120  125  130  135  140  145  150")

def main():
    """Run method for testing
    """
    display = Display()
    display.print_header()
    display.print_line()
    display.note_on(3)
    display.print_line()
    display.note_on(5)
    display.print_line()
    display.note_off(3)
    display.print_line()
    display.note_on(3)
    display.print_line()
    display.note_on(0)
    display.note_on(2)
    display.note_on(7)
    display.note_on(4)
    display.print_line()
    display.note_off(5)
    display.note_off(3)
    display.note_off(0)
    display.note_off(2)
    display.note_off(7)
    display.note_off(4)
    display.print_line()
    display.print_footer()

if __name__ == "__main__":
    main()
