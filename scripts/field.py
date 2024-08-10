import pygame.draw

from scripts.UI.text import Text
from scripts.settings import SIZE


class Field:

    def __init__(self):
        pass

    def draw(self, screen: pygame.Surface) -> None:
        Text("Press [Space] to quit...", [0, 0, 0], 50).print(screen, [SIZE[0]//2, SIZE[1]//2], True)

    def update(self) -> None:
        pass