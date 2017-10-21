"""Controls all basic functionality of the Raspberry Pi screen
like initialization, information display, and input.
"""
from typing import Tuple

import curses
import Adafruit_CharLCD as LCD


class Display:
    """Manages all display functionality.
    """
    # === Private Attributes ===
    # _lcd:
    #   the lcd display
    # _log:
    #   list of all strings displayed
    # _cur_index:
    #   where we are currently displaying in the log
    # _scrollable:
    #   boolean that dictates whether or not you can scroll through
    #   previous logs

    def __init__(self, initializers: Tuple[str, str] = ("", ""),
                       scrollable = False) -> None:
        """Initializes the display.
        """
        self._lcd = LCD.Adafruit_CharLCDPlate()
        self._log = list(initializers)
        self._cur_index = 1
        self._scrollable = scrollable
        self.clear()

    def clear(self) -> None:
        """Clears the display.
        """
        self._lcd.clear()

    def _put(self, line1: str, line2: str) -> None:
        """Puts each line onto the screen.
        """
        self._lcd.message(line1 + "\n" + line2)

    def show(self) -> None:
        """Shows the most recent two messages from <_log>.
        """
        self.clear()
        self._put(self._log[self._cur_index - 1], self._log[self._cur_index])

    def write(self, message: str) -> None:
        """Displays <message> at the bottom of the screen and appends
        it to <_log>.
        """
        self._log.append(message)
        self._cur_index += 1
        self.show()

    def scroll(self, displacement: int) -> None:
        """Scrolls through the log by <displacement>.
        Negative upwards, positive downwards.
        """
        self._cur_index = (displacement + self._cur_index) % len(self._log)
        self.show()

    def check_pressed(self) -> str:
        """Checks if any button has been pressed and returns a string
        representation of the button. If there is no button returns an
        empty string.
        """
        buttons = ((LCD.SELECT, "select"),
                   (LCD.LEFT,   "left"  ),
                   (LCD.UP,     "up"    ),
                   (LCD.DOWN,   "down"  ),
                   (LCD.RIGHT,  "right" ))
        
        for button in buttons:
            if self._lcd.is_pressed(button[0]):
                return button[1]
        return ""


class Input:
    """Manages all input using <curses>.
    """
    # === Private Attributes ===
    # _window:
    #   the curses window

    def __init__(self) -> None:
        """Initializes the input structure.
        """
        self._window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self._window.nodelay(True)

    def read(self) -> chr:
        """Gets the character input from the user and returns it.
        """
        get_chr = self._window.getch()
        # No character
        if get_chr == -1:
            return ''

        # Backspace
        if get_chr == 127:
            y, x = self._window.getyx()
            if x > 0:
                self._window.move(y, x - 1)
                self._window.delch(y, x - 1)
            return '\b'

        # Other
        self._window.addch(get_chr)
        return chr(get_chr)

    def stop(self) -> None:
        """Stops the curses input handler.
        """
        curses.echo()
        curses.nocbreak()
        curses.endwin()
