import pygame

import scripts.settings as s
from scripts.field import Field
from scripts.UI.text import Text


class App:

    def __init__(self) -> None:
        # Initialize pygame and settings
        pygame.init()

        self.size = self.width, self.height = s.SIZE
        self.name: str = s.NAME
        self.colors: dict = s.COLORS
        self.fps: int = s.FPS

        # Set pygame window
        pygame.display.set_caption(self.name)

        # Set pygame clock
        self.screen: pygame.Surface = pygame.display.set_mode(self.size, pygame.NOFRAME)
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Set input variables
        self.dt: int = 0
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.keys: list = []

        # This line takes data from save file
        self.field: Field = Field()

    def update(self) -> None:
        """
        Main update function of the program.
        This function is called every frame
        """

        # -*-*- Input Block -*-*-
        self.mouse_pos = pygame.mouse.get_pos()  # Get mouse position

        for event in pygame.event.get():  # Get all events
            if event.type == pygame.QUIT:  # If you want to close the program...
                close()

            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse button down...
                if event.button == 1:  # left click
                    NotImplementedError("Left click is not implemented yet")
                elif event.button == 3:  # right click...
                    NotImplementedError("Right click is not implemented yet")

            if event.type == pygame.KEYDOWN:  # If key button down...
                if event.key == pygame.K_SPACE:
                    close()

        self.keys = pygame.key.get_pressed()  # Get all keys (pressed or not)
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:  # If left arrow or 'a' is pressed...
            NotImplementedError("This button is not implemented yet")
        # -*-*-             -*-*-

        # -*-*- Physics Block -*-*-
        self.field.update()
        # -*-*-               -*-*-

        # -*-*- Rendering Block -*-*-
        self.screen.fill(self.colors['background'])  # Fill background
        self.field.draw(self.screen)

        fps_text = f"FPS: {self.clock.get_fps()}" if self.fps != 0 else "FPS: inf"
        Text(fps_text, [0, 0, 0], 20).print(self.screen, [self.width - 70, self.height - 21], False)  # FPS counter
        # -*-*-                 -*-*-

        # -*-*- Update Block -*-*-
        pygame.display.update()  # Update screen

        self.dt = self.clock.tick(self.fps)  # Get delta time based on FPS
        # -*-*-              -*-*-


def close() -> None:
    """
    Close the program
    :return:
    """

    pygame.quit()
    Text.FONTS = {}
    exit()
