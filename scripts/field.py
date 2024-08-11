import pygame.draw

from scripts import settings
from scripts.UI.text import Text
from scripts.settings import SIZE

import ctypes
import os

def get_wallpaper_path() -> str:
    if os.name != "nt":  # If we are not on Windows, we can't get the path to the wallpaper
        return ""
    SPI_GETDESKWALLPAPER = 0x0073
    buffer = ctypes.create_unicode_buffer(260)  # Maksymalna długość ścieżki to 260 znaków
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, len(buffer), buffer, 0)

    return buffer.value

def get_display_size():
    """
    This function returns the size of the display windows11
    """
    return (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))


class Field:

    def __init__(self):
        self.wallpaper = None
        self.update_wallpaper()

    def update_wallpaper(self) -> None:
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
            wallpaper = pygame.transform.scale(wallpaper, (window_width, window_height))
        except ValueError:
            wallpaper = pygame.transform.scale(self.wallpaper, (window_width, window_height))

        screen.blit(wallpaper, (0, 0))  # Draw wallpaper on screen

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, SIZE[0], SIZE[1]), 2)

    def update(self) -> None:
        pass