from scripts.UI.text import Text
from scripts.widgets.widget import Widget
from scripts.animations import timing_functions

from scripts.settings import SIZE
import pygame


class WeatherWidget(Widget):
    def __init__(self, name, pos) -> None:
        super().__init__(name, pos)

    def draw(self, widget_screen: pygame.Surface, shadow_screen: pygame.Surface) -> None:
        pygame.draw.circle(widget_screen, [255, 230, 0], [self.pos[0] + SIZE[0] * 0.28, self.pos[1] + SIZE[1] // 2], 50)
        Text("18°C", [0, 0, 0], 100).print(shadow_screen, [self.pos[0] + SIZE[0] * 0.66 + 3, self.pos[1] + SIZE[1] // 2 + 9], center=True)
        Text("18°C", [255, 255, 255], 100).print(widget_screen, [self.pos[0] + SIZE[0] * 0.66, self.pos[1] + SIZE[1] // 2 + 8], center=True)

    def start_animation(self, max_time: int, animation_type: int, start_after: int = 0):
        super().start_animation(max_time, animation_type, start_after)

    def update(self, dt: int):
        super().update(dt)
