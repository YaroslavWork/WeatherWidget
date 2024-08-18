from abc import ABC, abstractmethod

from scripts.animations import timing_functions
from scripts.settings import SIZE


class ANIMATION:
    IDLE = 0
    INSIDE_FROM_LEFT = 1
    INSIDE_FROM_RIGHT = 2
    OUTSIDE_TO_LEFT = 3
    OUTSIDE_TO_RIGHT = 4


class Widget(ABC):

    def __init__(self, name, start_pos):
        self.name = name
        self.pos = start_pos
        self.is_animation_started = False
        self.start_animation_time = 0
        self.max_animation_time = 0
        self.animation_type: int = ANIMATION.IDLE

    @abstractmethod
    def draw(self, widget_screen, shadow_screen):
        pass

    def start_animation(self, max_time, animation_type, start_after=0):
        self.is_animation_started = True
        self.start_animation_time = -start_after
        self.max_animation_time = max_time
        self.animation_type = animation_type

    def default_positon(self):
        if self.animation_type == ANIMATION.OUTSIDE_TO_LEFT:
            self.pos[0] = 0
        elif self.animation_type == ANIMATION.OUTSIDE_TO_RIGHT:
            self.pos[0] = 0
        elif self.animation_type == ANIMATION.INSIDE_FROM_LEFT:
            self.pos[0] = SIZE[0]
        elif self.animation_type == ANIMATION.INSIDE_FROM_RIGHT:
            self.pos[0] = -SIZE[0]

    def update(self, dt):
        if self.is_animation_started:
            self.start_animation_time += dt
            progress = self.start_animation_time / self.max_animation_time

            if self.start_animation_time < 0:  # Wait for start (if value is negative)
                self.default_positon()
                return

            if progress > 1:
                self.is_animation_started = False
                self.animation_type = ANIMATION.IDLE
                return

            if self.animation_type == ANIMATION.OUTSIDE_TO_LEFT:
                self.pos[0] = timing_functions.ease_in_animation(0, -SIZE[0], progress)
            elif self.animation_type == ANIMATION.OUTSIDE_TO_RIGHT:
                self.pos[0] = timing_functions.ease_in_animation(0, SIZE[0], progress)
            elif self.animation_type == ANIMATION.INSIDE_FROM_LEFT:
                self.pos[0] = timing_functions.ease_out_animation(-SIZE[0], 0, progress)
            elif self.animation_type == ANIMATION.INSIDE_FROM_RIGHT:
                self.pos[0] = timing_functions.ease_out_animation(SIZE[0], 0, progress)
