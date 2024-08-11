import math
import pygame


class SideButton:

    def __init__(self, center_angle: float, center_diff: float, size: float = 1, pos: tuple[int, int] = (0, 0)):
        self.center_angle = center_angle
        self.center_diff = center_diff
        self.size = size
        self.pos = pos
        self.button = []

    def create(self):
        radians = self.center_angle*math.pi/180
        left_radians = (self.center_angle - self.center_diff)*math.pi/180
        right_radians = (self.center_angle + self.center_diff)*math.pi/180
        vector1 = [[self.pos[0], self.pos[1]], [self.size*math.cos(left_radians)+self.pos[0], self.size*math.sin(left_radians)+self.pos[1]]]
        vector2 = [[self.pos[0], self.pos[1]], [self.size*math.cos(right_radians)+self.pos[0], self.size*math.sin(right_radians)+self.pos[1]]]
        self.button.append(vector1)
        self.button.append(vector2)

    def draw(self, screen: pygame.Surface, color: list[int, int, int]):
        for i in range(len(self.button)):
            pygame.draw.line(screen, color, self.button[i][0], self.button[i][1], 6)