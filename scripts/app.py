import sys

try:
    import moderngl
except ImportError:
    raise ImportError("Впиши 'pip install moderngl' в консоль")
import pygame
import array

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

        # Set pygame windows
        self.screen: pygame.Surface = pygame.display.set_mode(self.size, pygame.NOFRAME | pygame.OPENGL | pygame.DOUBLEBUF)
        self.UI_display: pygame.Surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)

        # Set pygame ctx and clock
        self.ctx = moderngl.create_context()
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Set input variables
        self.dt: int = 0
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.keys: list = []

        # This line takes data from save file
        self.field: Field = Field()

        # Set shader variables
        self.quad_buffer = self.ctx.buffer(array.array('f', [
            # position (x, y)  # texture (u, v)
            -1.0, 1.0, 0.0, 0.0,  # top left
            1.0, 1.0, 1.0, 0.0,  # top right
            -1.0, -1.0, 0.0, 1.0,  # bottom left
            1.0, -1.0, 1.0, 1.0,  # bottom right
        ]))

        vert_shader = open(f'{sys.path[0]}/scripts/shaders/vert_shader.glsl', 'r').read()
        frag_shader = open(f'{sys.path[0]}/scripts/shaders/frag_shader.glsl', 'r').read()

        self.program = self.ctx.program(
            vertex_shader=vert_shader,
            fragment_shader=frag_shader
        )
        self.render_object = self.ctx.vertex_array(
            self.program,
            [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')]
        )

    def surf_to_texture(self, surf: pygame.Surface) -> moderngl.Texture:
        """
        Convert pygame surface to moderngl texture
        """
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

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
        self.UI_display.fill(self.colors['background'])  # Fill background
        self.field.draw(self.UI_display)

        fps_text = f"FPS: {self.clock.get_fps()}" if self.fps != 0 else "FPS: inf"
        Text(fps_text, [0, 0, 0], 20).print(self.UI_display, [self.width - 70, self.height - 21], False)  # FPS counter
        # -*-*-                 -*-*-

        # -*-*- Shader Block -*-*-
        frame_tex = self.surf_to_texture(self.UI_display)

        frame_tex.use(1)
        self.program['uiTex'] = 1
        self.program['backgroundColor'] = (
            s.COLORS['background'][0] / 255,
            s.COLORS['background'][1] / 255,
            s.COLORS['background'][2] / 255
        )

        self.render_object.render(moderngl.TRIANGLE_STRIP)

        # -*-*- Update Block -*-*-
        pygame.display.flip()  # Update screen

        frame_tex.release()

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
