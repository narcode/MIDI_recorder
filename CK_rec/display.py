class Display:
    """The display class provides a clean output for the mdi signals.
    
    The ``notes_playing`` keeps track of all the notes that are currently 'on'.
    The ``print_line`` method will print a single line where the notes that are
    'on' are highlighted with an 'x'. Notes that are 'off' are marked with a
    normal space. By calling the ``print_line`` statement consecutive, you will
    gather a lint of midi-music of what you are playing. **NOTE:** only the
    note that are currently 'on' are printed, not the notes that fall between
    the time steps of the update procedure. Increase the time resolution to fix
    that.
    
    
    The methods ``note_on`` and ``note_off`` record the changes of the midi
    notes and they are set on the ``notes_playing`` variable. The method
    ``print_line`` will print an overview of that variable on the screen. You
    can obtain a ruler of the midi numbers with the ``print_header`` and
    ``print_footer`` methods.
    
    
    TODO:
    * add color
    
    
    Example: see the ``main`` method.
    """

    notes_playing = []     #array to track midi notes with on/off value
    MAX_MIDI_NOTES = 10    #should be 128 ?? number of midi notes available
    
    def __init__(self, note_on_symbol="x", note_off_symbol=" "):
        """Initialise the class and set variables.
        """
        self._note_on_symbol = note_on_symbol
        self._note_off_symbol = note_off_symbol
        self.notes_playing = [False for x in range(0,self.MAX_MIDI_NOTES)]

    def _check_note_range(self, midinumber):
        """Helper function to check if midinumber is valid.
        
        :param int midinumber: the midi not number to check
        :return boolean: True if succesful
        """
        #TODO: is 0 allowed?
        if (midinumber < 0 and midinumber >self.MAX_MIDI_NOTES):
            raise  TypeError("Invalid midi number")
        return True
    
    def note_on(self, midinumber):
        """Register the note with midinumber to on.
        
        :param int midinumber: the midinumber of the note being played
        """
        self._check_note_range(midinumber)
        self.notes_playing[midinumber] = True
    
    def note_off(self, midinumber):
        """Register the note with midinumber to off.
        
        :param int midinumber: the midinumber of the note not played anymore
        """
        self._check_note_range(midinumber)
        self.notes_playing[midinumber] = False
    
    def print_line(self):
        """Print a single line with the midi notes
        """
        buildstring = [self._note_on_symbol if x else self._note_off_symbol
                        for x in self.notes_playing]
        print("".join(buildstring))

    def print_header(self):
        """Print a header line.
        
        This should help you to navigate between midinumbers.
        """
        print("1    5    10   11   15   20   25   30   35   40   45   50   " \
             +"55   60   65   70   75   80   85   90   95   100  105  110  " \
             +"115  120  125  130  135  140  145  150")
        print("|____|____|____|____|____|____|____|____|____|____|____|____" \
             +"|____|____|____|____|____|____|____|____|____|____|____|____" \
             +"|____|____|____|____|____|____|____|")

    def print_footer(self):
        """Print a footer line.
        
        This should help you to navigate between midinumbers.
        """
        print(" ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____" \
             +" ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____" \
             +" ____ ____ ____ ____ ____ ____ ____")
        print("|    |    |    |    |    |    |    |    |    |    |    |    " \
             +"|    |    |    |    |    |    |    |    |    |    |    |    " \
             +"|    |    |    |    |    |    |    |")
        print("1    5    10   11   15   20   25   30   35   40   45   50   " \
             +"55   60   65   70   75   80   85   90   95   100  105  110  " \
             +"115  120  125  130  135  140  145  150")

def main():
    """Run method for testing
    
    This doesn't record anything, just testing the display. It should print
    something like (depending on the settings):
    
     1    5    10   11   15   20   25
     |____|____|____|____|____|____|
               
       x      
       x x    
         x    
       x x    
    x xxxx x  
              
     ____ ____ ____ ____ ____ ____
    |    |    |    |    |    |    |
    1    5    10   11   15   20   25
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
