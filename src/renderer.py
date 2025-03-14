from pathlib import Path
from time import time
from typing import *

import moderngl as mgl
import moderngl_window as mglw
from moderngl_window.integrations.imgui_bundle import ModernglWindowRenderer

from imgui_bundle import imgui

import numpy as np

class FractalRenderer(mglw.WindowConfig):
    gl_version = (4, 0) # version 400
    title = "Musique Fractale"
    window_size = (800, 450)
    aspect_ratio = None
    resource_dir = shaderDir = (Path(__file__) / "../../shaders").resolve()
    mousePosition = (0, 0)
    imgui: ModernglWindowRenderer

    fractalsVA: Dict[str, mgl.VertexArray] = {}
    currentFractal: str
    julia: bool = False
    juliaC = [0., 0.]
    smoothing = False

    nthMandelbrotPower = 2
    nthMandelbrotAnimation = False
    nthMandelbrotAnimationSpeed = 0.1

    center = [0., 0.]
    # distance sur le plan complexe entre le haut et le bas de l'écran
    # diminuer pour zoomer ; augmenter pour dézoomer
    zoom = 2.
    limit = 100

    colorGradient = (66/255,  30/255,  15/255), (25/255,  7/255,   26/255), (9/255,   1/255,   47/255), \
                    (4/255,   4/255,   73/255), (0/255,   7/255,   100/255),(12/255,  44/255,  138/255), \
                    (24/255,  82/255,  177/255),(57/255,  125/255, 209/255),(134/255, 181/255, 229/255), \
                    (211/255, 236/255, 248/255),(241/255, 233/255, 191/255),(248/255, 201/255, 95/255), \
                    (255/255, 170/255, 0/255),  (204/255, 128/255, 0/255),  (153/255, 87/255,  0/255), \
                    (106/255, 52/255,  3/255)

    # les vertices de 2 triangles incluant tout l'écran
    screenVertices = np.array((
        -1.0,  1.0,
        -1.0, -1.0,
         1.0, -1.0,

        -1.0,  1.0,
         1.0,  1.0,
         1.0, -1.0,
    ))
    screenVB: mgl.Buffer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)
        
        io = imgui.get_io()
        io.font_global_scale = 1.4

        self.screenVB = self.ctx.buffer(self.screenVertices.astype("f4").tobytes(), 0, True)

        self.loadFractale("mandelbrot")
        self.loadFractale("nthMandelbrot")
        self.loadFractale("burningShip")

        self.currentFractal = "mandelbrot"
        self.update_fractal()

    def loadFractale(self, name: str):
        print({name.upper():1})
        program = self.load_program(path="fractal.glsl", defines={name.upper():"1"})
        program["colorGradient"] = self.colorGradient
        self.fractalsVA[name] = self.ctx.vertex_array(program, self.screenVB, "in_vert")

    def currentVA(self) -> mgl.VertexArray:
        return self.fractalsVA[self.currentFractal]

    def update_fractal(self):
        p = self.currentVA().program
        p["screenSize"] = self.wnd.size
        p["center"] = self.center
        p["zoom"] = self.zoom * self.wnd.size[0] / self.wnd.size[1], self.zoom
        p["limit"] = self.limit
        p["smoothing"] = self.smoothing
        p["julia"] = self.julia
        if self.currentFractal == "nthMandelbrot":
            p["power"] = self.nthMandelbrotPower
            p["halvedPower"] = self.nthMandelbrotPower / 2
        if self.julia:
            p["juliaC"] = self.juliaC

    def resetZoom(self):
        "Il faut appeler update_fractal après pour que cette function fasse effet"
        self.zoom = 2
        self.center = [0, 0]

    def on_render(self, currentTime, deltaTime):
        self.wnd.clear()
        self.currentVA().render(mgl.TRIANGLES)

        self.renderUi(currentTime, deltaTime)

        if self.nthMandelbrotAnimation:
            self.nthMandelbrotPower += self.nthMandelbrotAnimationSpeed * deltaTime
            self.update_fractal()

    def fNumber(self, x: float) -> str:
        if x == 0: return "0"
        a = np.abs(x)
        if a < 10 and a > 0.01: return str(np.round(x, 4))
        return np.format_float_scientific(x, 2)

    def renderUi(self, currentTime, deltaTime):
        imgui.new_frame()

        imgui.set_next_window_pos((0, 0), imgui.Cond_.appearing)
        imgui.begin("Paramètres", None,
                    imgui.WindowFlags_.no_move | imgui.WindowFlags_.always_auto_resize)

        imgui.text(f"FPS: {np.round(self.timer.fps, 1)}")
        screenRatio = self.wnd.size[0] / self.wnd.size[1]
        x = (self.mousePosition[0] / self.wnd.size[0] - 0.5) * self.zoom * screenRatio + self.center[0]
        y = -(self.mousePosition[1] / self.wnd.size[1] - 0.5) * self.zoom + self.center[1]
        imgui.text(f"Position: {self.fNumber(x)} + {self.fNumber(y)}i")

        if (imgui.begin_combo("##", self.currentFractal)):
            for name in self.fractalsVA.keys():
                imgui.push_id(name)
                selected = name == self.currentFractal
                s = imgui.selectable(name, selected)
                if s[1] and not selected:
                    self.currentFractal = name
                    self.resetZoom()
                    self.update_fractal()
                imgui.pop_id()

            imgui.end_combo()

        imgui.text(f"  Nom: {"test"}")
        imgui.text(f"  Centre: {self.fNumber(self.center[0])} + {self.fNumber(self.center[1])}i")
        imgui.text(f"  Zoom: {self.fNumber(self.zoom)}")
        imgui.text(f"  Précision")
        imgui.same_line()
        s = imgui.slider_int("##Limit", self.limit, 10, 100000, flags=imgui.SliderFlags_.logarithmic)
        if (s[0]):
            self.limit = s[1]
            self.update_fractal()
        
        imgui.text(f"  Dégradé")
        imgui.same_line()
        c = imgui.checkbox("##Smoothing", self.smoothing)
        if (c[0]):
            self.smoothing = c[1]
            self.update_fractal()
        
        if (self.julia):
            imgui.text(f"  Julia C: {self.fNumber(self.juliaC[0])} + {self.fNumber(self.juliaC[1])}i")

        if (self.currentFractal == "nthMandelbrot"):
            imgui.text(f"  Puissance")
            imgui.same_line()
            s = imgui.slider_float("##Power", self.nthMandelbrotPower, 2, 10)
            if (s[0]):
                self.nthMandelbrotPower = s[1]
                self.update_fractal()

            imgui.text(f"  Animation")
            imgui.same_line()
            c = imgui.checkbox("##Animation", self.nthMandelbrotAnimation)
            if (c[0]):
                self.nthMandelbrotAnimation = c[1]
                self.update_fractal()

            imgui.text(f"  Vitesse: ")
            imgui.same_line()
            s = imgui.slider_float("##Vitesse", self.nthMandelbrotAnimationSpeed, 0.05, 1)
            if (s[0]):
                self.nthMandelbrotAnimationSpeed = s[1]
                self.update_fractal()

        imgui.end()

        test = imgui.get_background_draw_list()
        test.add_circle_filled((0, 0), 50, 0xffff)

        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    def on_resize(self, width, height):
        self.update_fractal()
        self.imgui.resize(width, height)

    def on_key_event(self, key, action, modifiers):
        self.imgui.key_event(key, action, modifiers)

    def on_mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)
        self.mousePosition = (x, y)

    def on_mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)
        self.mousePosition = (x, y)

        self.center[0] += -dx * self.zoom / self.wnd.size[1]
        self.center[1] += dy * self.zoom / self.wnd.size[1]

        self.update_fractal()

    def on_mouse_scroll_event(self, x_offset: float, y_offset: float):
        self.imgui.mouse_scroll_event(x_offset, y_offset)
        oldZoom = self.zoom
        self.zoom /= 1.1 ** y_offset

        screenRatio = self.wnd.size[0] / self.wnd.size[1]
        self.center[0] += (self.mousePosition[0] / self.wnd.size[0] - 0.5) * (oldZoom - self.zoom) * screenRatio
        self.center[1] += -(self.mousePosition[1] / self.wnd.size[1] - 0.5) * (oldZoom - self.zoom)

        self.update_fractal()

    def on_mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

        if button == 2:
            if not self.julia:
                screenRatio = self.wnd.size[0] / self.wnd.size[1]
                self.juliaC[0] = (x / self.wnd.size[0] - 0.5) * self.zoom * screenRatio + self.center[0]
                self.juliaC[1] = -(y / self.wnd.size[1] - 0.5) * self.zoom + self.center[1]
                self.julia = True
                self.resetZoom()

            elif self.julia:
                self.julia = False
                self.resetZoom()
            
            self.update_fractal()


    def on_mouse_release_event(self, x, y, button):
        self.imgui.mouse_release_event(x, y, button)

    def on_unicode_char_entered(self, char):
        self.imgui.unicode_char_entered(char)