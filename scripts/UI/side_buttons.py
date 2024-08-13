import math
import pygame

from scripts.animations import timing_functions


class SideButton:
    animation_diff = 20
    animation_duration = 250

    def __init__(self, center_angle: float, center_diff: float, size: float = 1, pos: tuple[int, int] = (0, 0)):
        self.center_angle = center_angle
        self.center_diff = center_diff
        self.size = size
        self.pos = pos
        self.button = []
        self.is_hover = False
        self.is_clicked = False
        self.last_click_time = 0

    def create(self, diff):
        self.button = []
        left_radians = (self.center_angle - diff)*math.pi/180
        right_radians = (self.center_angle + diff)*math.pi/180
        vector1 = [[self.pos[0], self.pos[1]], [self.size*math.cos(left_radians)+self.pos[0], self.size*math.sin(left_radians)+self.pos[1]]]
        vector2 = [[self.pos[0], self.pos[1]], [self.size*math.cos(right_radians)+self.pos[0], self.size*math.sin(right_radians)+self.pos[1]]]
        self.button.append(vector1)
        self.button.append(vector2)

    def click_down(self):
        if self.is_hover:
            self.is_clicked = True
            self.last_click_time = 0

    def click_up(self):
        if self.is_clicked:
            self.is_clicked = False
            self.last_click_time = 0

    def draw(self, screen: pygame.Surface, color: list[int, int, int]):
        for i in range(len(self.button)):
            pygame.draw.line(screen, color, self.button[i][0], self.button[i][1], 6)

    def update(self, dt, mouse_pos):
        positions_x = self.button[0][0][0], self.button[0][1][0], self.button[1][0][0], self.button[1][1][0]
        positions_y = self.button[0][0][1], self.button[0][1][1], self.button[1][0][1], self.button[1][1][1]
        # Make a rectangle from the button
        min_x, max_x = min(positions_x)-5, max(positions_x)+5
        min_y, max_y = min(positions_y)-5, max(positions_y)+5
        if min_x <= mouse_pos[0] <= max_x and min_y <= mouse_pos[1] <= max_y:
            self.is_hover = True
        else:
            self.is_hover = False

        self.last_click_time += dt
        if self.is_clicked:
            if self.last_click_time >= SideButton.animation_duration:
                self.create(self.center_diff-SideButton.animation_diff)
            else:
                self.create(timing_functions.ease_out_animation(self.center_diff,
                                                                self.center_diff-SideButton.animation_diff,
                                                                self.last_click_time/SideButton.animation_duration))
        else:
            if self.last_click_time >= SideButton.animation_duration:
                self.create(self.center_diff)
            else:
                self.create(timing_functions.ease_out_animation(self.center_diff-SideButton.animation_diff,
                                                                self.center_diff,
                                                                self.last_click_time/SideButton.animation_duration))