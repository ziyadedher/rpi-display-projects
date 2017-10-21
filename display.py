"""Displays text as is on the LCD 16x2 display.

Can be used interactively or one-time through the command line.
"""
from typing import List

import sys
import controller


class Writer:
    """Manages all interactivity or one-time display.
    """
    # === Private Attributes ===
    # _display:
    #   the lcd display controller

    def __init__(self) -> None:
        """Initializes the writer.
        """
        self._display = controller.Display()

    def write(self, lines: List[str]) -> None:
        """Writes out the list <lines> to screen in order.
        """
        for line in lines:
            self._display.write(line)

    def start_interactive(self, num_inputs: int = 0,
                                stop_keyword: str = "__END__") -> None:
        """Begins the interactive display.

        Stops after a number of inputs <num_inputs> (default 0 for no end)
        and/or when a <stop_keyword> is typed (default '__END__').
        """
        
        num = 0
        message = ""
        while num_inputs == 0 or num < num_inputs:
            num += 1

            message = str(input())
            if message == stop_keyword:
                break

            self.write(message)


if __name__ == "__main__":
    writer = Writer()
    if len(sys.argv) > 1:
        writer.write(sys.argv[1:])
    else:
        writer.start_interactive()
