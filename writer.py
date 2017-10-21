"""Displays text as is on the LCD 16x2 display.

Can be used interactively or one-time through the command line.
"""
from typing import List

import sys
import time
import controller


class Writer:
    """Manages all interactivity or one-time display.
    """
    # === Private Attributes ===
    # _display:
    #   the lcd display controller
    # _input:
    #   the input controller
    # _delay:
    #   buffer time until accepting a new button press
    #   after receiving one

    def __init__(self, delay = 0.1) -> None:
        """Initializes the writer.
        """
        self._display = controller.Display()
        self._input = controller.Input()
        self._delay = delay
        
    def end(self) -> None:
        """Ends the writer.
        """
        self._input.stop()

    def show(self, lines: List[str]) -> None:
        """Shows the list <lines> to screen in order.
        """
        for line in lines:
            self._display.write(line)

    def _check_plate_input(self) -> None:
        """Checks plate input and reacts accordingly by scrolling
        or other functionality.
        """
        button = self._display.check_pressed()
        if button == "":
            return
        elif button == "select":
            pass
        elif button == "left":
            pass
        elif button == "up":
            self._display.scroll(-1)
            time.sleep(self._delay)
        elif button == "down":
            self._display.scroll(1)
            time.sleep(self._delay)
        elif button == "right":
            pass


    def start_interactive(self, num_inputs: int = 0,
                                stop_keyword: str = "__END__") -> None:
        """Begins the interactive display.

        Stops after a number of inputs <num_inputs> (default 0 for no end)
        and/or when a <stop_keyword> is typed (default '__END__').
        """
        num = 0
        message = ""
        try:
            while num_inputs == 0 or num < num_inputs:
                read = self._input.read()
                
                # No input
                if read == '':
                    pass

                # Backspace
                elif read == '\b':
                    message = message[:-1]

                # Enter
                elif read == '\n':
                    num += 1
                    if message == stop_keyword:
                        raise KeyboardInterrupt
                    self.show([message])
                    message = ""
                
                # Other
                else:
                    message += read

                self._check_plate_input()

        except KeyboardInterrupt:
            self.end()
            sys.exit()


if __name__ == "__main__":
    writer = Writer()
    if len(sys.argv) > 1:
        writer.show(sys.argv[1:])
    else:
        writer.start_interactive()
    writer.end()
