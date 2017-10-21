"""Controls all basic functionality of the Raspberry Pi screen
like initialization and information display.
"""
from typing import Tuple

import Adafruit_CharLCD as LCD


class Display:
    """Manages all display functionality.
    """
    # === Private Attributes ===
    # _lcd:
    #   the lcd display
    # _log:
    #   list of all strings displayed

    def __init__(self, initializers: Tuple[str, str] = ("", "")) -> None:
        """Initializes the display.
        """
        self._lcd = LCD.Adafruit_CharLCDPlate()
        self._log = list(initializers)
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
        self._put(self._log[-2], self._log[-1])

    def write(self, message: str) -> None:
        """Displays <message> at the bottom of the screen and appends
        it to <_log>.
        """
        self._log.append(message)
        self.clear()
        self._put(self._log[-2], self._log[-1])
