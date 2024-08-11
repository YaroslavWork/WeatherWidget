import os
from scripts import field, app

if __name__ == "__main__":
    print(f"Os name: {os.name}")
    print(f"Wallpaper path: {field.get_wallpaper_path()}")
    print(f"Display size: {field.get_display_size()}")
    App = app.App()
    while True:
        App.update()
        print(f"Screen position: {App.screen_pos}")
