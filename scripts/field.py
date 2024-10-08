import subprocess

import pygame.draw

from scripts import settings
from scripts.UI.side_buttons import SideButton
from scripts.UI.text import Text
from scripts.settings import SIZE

import ctypes
import os

from scripts.widgets.weather_widget import WeatherWidget
from scripts.widgets.widget import ANIMATION


def get_wallpaper_path() -> str:
    if os.name == "nt":  # If we are not on Windows, we can't get the path to the wallpaper
        SPI_GETDESKWALLPAPER = 0x0073
        buffer = ctypes.create_unicode_buffer(260)  # Maximum length of the path is 260 characters
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, len(buffer), buffer, 0)
        return buffer.value
    elif os.name == "posix":  # macOS (eventually Linux)
        try:
            if subprocess.run(['uname'], capture_output=True, text=True).stdout.strip() == "Darwin":
                script = """
                    tell application "System Events"
                        tell current desktop
                            set wallpaperPath to picture as text
                        end tell
                    end tell
                    """
                result = subprocess.run(
                    ['osascript', '-e', script],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    return result.stdout.strip().replace(":", "/").replace("Macintosh HD", "")
        except Exception as e:
            return f"Error retrieving wallpaper path on macOS: {e}"

    return ""  # If the OS is neither Windows nor macOS or in case of an error


def get_display_size() -> tuple[int, int]:
    """
    This function returns the size of the display (width, height)
    """
    if os.name == "nt":  # Windows
        return ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
    elif os.name == "posix":  # macOS (eventually Linux)
        try:
            if subprocess.run(['uname'], capture_output=True, text=True).stdout.strip() == "Darwin":
                import Quartz
                main_monitor = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
                width = int(main_monitor.size.width)
                height = int(main_monitor.size.height)
                return width, height
        except Exception as e:
            raise Exception(f"Error retrieving display size on macOS: {e}")

    return 0, 0  # If the OS is neither Windows nor macOS or in case of an error


class Field:

    def __init__(self) -> None:
        self.wallpaper = None
        self.update_wallpaper()

        self.left_button = SideButton(0, 60, 20, (SIZE[0] * 0.05, SIZE[1] // 2))
        self.left_button.create(60)
        self.right_button = SideButton(180, 60, 20, (SIZE[0] * 0.95, SIZE[1] // 2))
        self.right_button.create(60)
        self.bottom_button = SideButton(90, 80, 30, (SIZE[0] // 2, SIZE[1] * 0.85))
        self.bottom_button.create(80)

        self.widgets = [WeatherWidget("Weather", [0, 0]), WeatherWidget("Weather", [500, 0])]
        self.active_widget = 0

    def update_wallpaper(self) -> None:
        if os.name == "nt":
            self.wallpaper = pygame.image.load(get_wallpaper_path())

    def draw_wallpaper(self, screen: pygame.Surface, screen_pos: tuple[int, int], is_windowless: bool) -> None:
        display_size = get_display_size()
        wallpaper_width, wallpaper_height = self.wallpaper.get_size()
        window_width, window_height = settings.SIZE

        pos_x = screen_pos[0] * wallpaper_width / display_size[0]
        pos_y = screen_pos[1] * wallpaper_height / display_size[1]

        wallpaper_width = wallpaper_width * window_width / display_size[0]
        wallpaper_height = wallpaper_height * window_height / display_size[1]

        if not is_windowless:
            pos_y += 30 * wallpaper_height / window_height
            pos_x += 10 * wallpaper_width / window_width

        try:
            wallpaper = self.wallpaper.subsurface(pygame.Rect(pos_x, pos_y, wallpaper_width, wallpaper_height))
            wallpaper = pygame.transform.scale(wallpaper, [window_width, window_height])
        except ValueError:
            wallpaper = pygame.transform.scale(self.wallpaper, [window_width, window_height])

        screen.blit(wallpaper, [0, 0])  # Draw wallpaper on screen

    def change_widget(self, is_left: bool) -> None:
        if is_left:
            next_widget = (self.active_widget + 1) % len(self.widgets)
            self.widgets[self.active_widget].start_animation(750, ANIMATION.OUTSIDE_TO_LEFT, start_after=0)
            self.widgets[next_widget].start_animation(750, ANIMATION.INSIDE_FROM_RIGHT, start_after=300)
        else:
            next_widget = (self.active_widget - 1) % len(self.widgets)
            self.widgets[self.active_widget].start_animation(750, ANIMATION.OUTSIDE_TO_RIGHT, start_after=0)
            self.widgets[next_widget].start_animation(750, ANIMATION.INSIDE_FROM_LEFT, start_after=300)

        self.active_widget = next_widget

    def draw(self, screen: pygame.Surface, shadow_screen: pygame.Surface) -> None:
        for widget in self.widgets:
            widget.draw(screen, shadow_screen)

    def button_draw(self, screen: pygame.Surface) -> None:
        self.left_button.draw(screen, [255, 255, 255])
        self.right_button.draw(screen, [255, 255, 255])
        self.bottom_button.draw(screen, [255, 255, 255])

    def update(self, dt) -> None:
        self.left_button.update(dt)
        self.right_button.update(dt)
        self.bottom_button.update(dt)

        for widget in self.widgets:
            widget.update(dt)

    def click_down(self, mouse_pos) -> None:
        self.left_button.click_down(mouse_pos)
        self.right_button.click_down(mouse_pos)
        self.bottom_button.click_down(mouse_pos)

    def click_up(self, mouse_pos) -> None:
        self.left_button.click_up(mouse_pos, lambda: self.change_widget(is_left=True))
        self.right_button.click_up(mouse_pos, lambda: self.change_widget(is_left=False))
        self.bottom_button.click_up(mouse_pos, lambda: None)
