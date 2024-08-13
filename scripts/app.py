import ctypes
import math
import os
import sys

from scripts.animations import timing_functions

try:
    if os.name == "nt":
        import moderngl
except ImportError:
    raise ImportError("Впиши 'pip install moderngl' в консоль")
import pygame
import array

import scripts.settings as s
from scripts.field import Field
from scripts.UI.text import Text


class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long)
    ]


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
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Set input variables
        self.dt: int = 0
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.keys: list = []
        self.is_windowless: bool = True
        self.left_click_pressed: bool = False
        self.left_click_pressed_time: int = 0
        self.mouse_outside: bool = False
        self.mouse_outside_time: int = 0

        self.show_fps: bool = False

        # This line takes data from save file
        self.field: Field = Field()

    def update(self) -> None:
        pass


class AppWindows(App):

    def __init__(self) -> None:
        super().__init__()

        # Set moderngl context
        self.screen = pygame.display.set_mode(self.size, pygame.OPENGL | pygame.DOUBLEBUF | pygame.NOFRAME)
        self.background_display = pygame.Surface(self.size, pygame.SRCALPHA)
        self.UI_display = pygame.Surface(self.size, pygame.SRCALPHA)
        self.shadow_display = pygame.Surface(self.size, pygame.SRCALPHA)
        self.buttons_display = pygame.Surface(self.size, pygame.SRCALPHA)
        self.app_shadow_display = pygame.Surface(self.size, pygame.SRCALPHA)
        self.ctx = moderngl.create_context()

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

    def screen_pos_in_windows(self):
        """
        This function returns the position of the window on the screen (WORK ONLY ON WINDOWS)
        """
        window = pygame.display.get_wm_info()['window']
        rect = RECT()
        ctypes.windll.user32.GetWindowRect(window, ctypes.byref(rect))
        self.screen_pos = (x := rect.left, y := rect.top)

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
        mouse_pos_ratio = (self.mouse_pos[0] / self.width, self.mouse_pos[1] / self.height)
        if mouse_pos_ratio[0] <= 0 or mouse_pos_ratio[0] >= 0.997 or mouse_pos_ratio[1] <= 0 or mouse_pos_ratio[1] >= 0.992:
            self.mouse_outside = True
        else:
            self.mouse_outside = False
            self.mouse_outside_time = 0

        for event in pygame.event.get():  # Get all events
            if event.type == pygame.QUIT:  # If you want to close the program...
                close()

            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse button down...
                if event.button == 1:  # left click
                    self.left_click_pressed = True
                    self.field.update_wallpaper()
                    self.field.click_down()
                    # self.is_windowless = not self.is_windowless
                    # if self.is_windowless:
                    #     self.screen = pygame.display.set_mode(self.size, pygame.NOFRAME | pygame.OPENGL | pygame.DOUBLEBUF)
                    # else:
                    #     self.screen = pygame.display.set_mode(self.size, pygame.OPENGL | pygame.DOUBLEBUF)
                elif event.button == 3:  # right click...
                    NotImplementedError("Right click is not implemented yet")
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_click_pressed = False
                    self.left_click_pressed_time = 0
                    self.field.click_up()

            if event.type == pygame.KEYDOWN:  # If key button down...
                if event.key == pygame.K_SPACE:
                    close()
                if event.key == pygame.K_f:
                    self.show_fps = not self.show_fps

        self.keys = pygame.key.get_pressed()  # Get all keys (pressed or not)
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:  # If left arrow or 'a' is pressed...
            NotImplementedError("This button is not implemented yet")
        # -*-*-             -*-*-

        # -*-*- Physics Block -*-*-
        self.screen_pos_in_windows()
        self.field.update(self.dt, self.mouse_pos)
        if self.left_click_pressed:
            self.left_click_pressed_time += self.dt
        if self.mouse_outside:
            self.mouse_outside_time += self.dt
        # -*-*-               -*-*-

        # -*-*- Rendering Block -*-*-
        self.background_display.fill(self.colors['background'])  # Fill background
        self.UI_display.fill((0, 0, 0, 0))
        self.buttons_display.fill((0, 0, 0, 0))
        self.shadow_display.fill((0, 0, 0, 0))
        self.app_shadow_display.fill((0, 0, 0, 0))

        self.field.draw_wallpaper(self.background_display, self.screen_pos, self.is_windowless)
        self.field.draw(self.UI_display, self.shadow_display)
        self.field.button_draw(self.buttons_display)

        pygame.draw.line(self.app_shadow_display, (0, 0, 0), [self.width*0.025, self.height*0.96], [self.width*0.985, self.height*0.96], 3)
        pygame.draw.line(self.app_shadow_display, (0, 0, 0), [self.width*0.985, self.height*0.96], [self.width*0.985, self.height*0.065], 3)

        if self.show_fps:
            fps_text = f"FPS: {self.clock.get_fps()}"
            Text(fps_text, [0, 0, 0], 20).print(self.UI_display, [self.width - 70, self.height - 21], False)  # FPS counter
        # -*-*-                 -*-*-

        # -*-*- Shader Block -*-*-
        frame_tex1 = self.surf_to_texture(self.background_display)
        frame_tex2 = self.surf_to_texture(self.UI_display)
        frame_tex3 = self.surf_to_texture(self.buttons_display)
        frame_tex4 = self.surf_to_texture(self.shadow_display)
        frame_tex5 = self.surf_to_texture(self.app_shadow_display)

        frame_tex1.use(1)
        self.program['backgroundTex'] = 1
        frame_tex2.use(2)
        self.program['uiTex'] = 2
        frame_tex3.use(3)
        self.program['buttonsTex'] = 3
        frame_tex4.use(4)
        self.program['shadowTex'] = 4
        frame_tex5.use(5)
        self.program['appShadowTex'] = 5
        self.program['backgroundColor'] = (
            s.COLORS['background'][0] / 255,
            s.COLORS['background'][1] / 255,
            s.COLORS['background'][2] / 255
        )
        self.program['resolution'] = (self.width, self.height)
        self.program['mousePos'] = mouse_pos_ratio
        self.program['mouseOutsideTime'] = self.mouse_outside_time / 1000

        self.render_object.render(moderngl.TRIANGLE_STRIP)

        # -*-*- Update Block -*-*-
        pygame.display.flip()  # Update screen

        frame_tex1.release()
        frame_tex2.release()
        frame_tex3.release()
        frame_tex4.release()
        frame_tex5.release()

        self.dt = self.clock.tick(self.fps)  # Get delta time based on FPS
        # -*-*-              -*-*-


class AppLinux(App):

    def __init__(self) -> None:
        super().__init__()

        self.screen: pygame.Surface = pygame.display.set_mode(self.size, pygame.NOFRAME)

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
                    self.is_windowless = not self.is_windowless
                    if self.is_windowless:
                        self.screen = pygame.display.set_mode(self.size, pygame.NOFRAME)
                    else:
                        self.screen = pygame.display.set_mode(self.size)
                elif event.button == 3:  # right click...
                    NotImplementedError("Right click is not implemented yet")

            if event.type == pygame.KEYDOWN:  # If key button down...
                if event.key == pygame.K_SPACE:
                    close()
                if event.key == pygame.K_f:
                    self.show_fps = not self.show_fps

        self.keys = pygame.key.get_pressed()  # Get all keys (pressed or not)
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:  # If left arrow or 'a' is pressed...
            NotImplementedError("This button is not implemented yet")
        # -*-*-             -*-*-

        # -*-*- Physics Block -*-*-
        self.field.update(self.dt)
        # -*-*-               -*-*-

        # -*-*- Rendering Block -*-*-
        self.screen.fill(self.colors['background'])  # Fill background
        self.field.draw(self.screen)
        self.field.button_draw(self.screen)

        if self.show_fps:
            fps_text = f"FPS: {int(self.clock.get_fps())}" if self.clock.get_fps() != math.inf else "FPS: inf"
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
