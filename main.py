# Weather widget for Windows
# Python version: 3.11.2

from scripts.app import App

if __name__ == "__main__":
    app = App()

    while True:
        app.update()