# Weather widget for Windows
# Python version: 3.11.2
import os

from scripts.app import AppWindows, AppLinux

if __name__ == "__main__":
    app = None
    if os.name != "nt":  # Windows
        app = AppWindows()
    elif os.name != "posix":  # Linux (and potentially macOS)
        app = AppLinux()

    while True:
        app.update()
