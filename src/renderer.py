from pathlib import Path

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

    mandelbrotVA: mgl.VertexArray
    mandelbrotGradient = (66/255,  30/255,  15/255), (25/255,  7/255,   26/255), (9/255,   1/255,   47/255), \
                         (4/255,   4/255,   73/255), (0/255,   7/255,   100/255),(12/255,  44/255,  138/255), \
                         (24/255,  82/255,  177/255),(57/255,  125/255, 209/255),(134/255, 181/255, 229/255), \
                         (211/255, 236/255, 248/255),(241/255, 233/255, 191/255),(248/255, 201/255, 95/255), \
                         (255/255, 170/255, 0/255),  (204/255, 128/255, 0/255),  (153/255, 87/255,  0/255), \
                         (106/255, 52/255,  3/255)

    nthMandelbrotVA: mgl.VertexArray
    nthMandelbrotGradient = (66/255,  30/255,  15/255), (25/255,  7/255,   26/255), (9/255,   1/255,   47/255), \
                            (4/255,   4/255,   73/255), (0/255,   7/255,   100/255),(12/255,  44/255,  138/255), \
                            (24/255,  82/255,  177/255),(57/255,  125/255, 209/255),(134/255, 181/255, 229/255), \
                            (211/255, 236/255, 248/255),(241/255, 233/255, 191/255),(248/255, 201/255, 95/255), \
                            (255/255, 170/255, 0/255),  (204/255, 128/255, 0/255),  (153/255, 87/255,  0/255), \
                            (106/255, 52/255,  3/255)
    nthMandelbrotPower = 2

    juliaVA: mgl.VertexArray
    juliaGradient = (66/255,  30/255,  15/255), (25/255,  7/255,   26/255), (9/255,   1/255,   47/255), \
                            (4/255,   4/255,   73/255), (0/255,   7/255,   100/255),(12/255,  44/255,  138/255), \
                            (24/255,  82/255,  177/255),(57/255,  125/255, 209/255),(134/255, 181/255, 229/255), \
                            (211/255, 236/255, 248/255),(241/255, 233/255, 191/255),(248/255, 201/255, 95/255), \
                            (255/255, 170/255, 0/255),  (204/255, 128/255, 0/255),  (153/255, 87/255,  0/255), \
                            (106/255, 52/255,  3/255)
    juliaC = [0., 0.]

    currentVA: mgl.VertexArray

    center = [0., 0.]
    # distance sur le plan complexe entre le haut et le bas de l'écran
    # diminuer pour zoomer ; augmenter pour dézoomer
    zoom = 2.
    limit = 5000

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

        self.screenVB = self.ctx.buffer(self.screenVertices.astype("f4").tobytes(), 0, True)

        mandelbrot = self.load_program(vertex_shader = "fractal.vert", fragment_shader = "mandelbrot.frag")
        mandelbrot["colorGradient"] = self.mandelbrotGradient
        self.mandelbrotVA = self.ctx.vertex_array(mandelbrot, self.screenVB, "in_vert")

        nthMandelbrot = self.load_program(vertex_shader = "fractal.vert", fragment_shader = "nthMandelbrot.frag")
        nthMandelbrot["colorGradient"] = self.nthMandelbrotGradient
        self.nthMandelbrotVA = self.ctx.vertex_array(nthMandelbrot, self.screenVB, "in_vert")

        julia = self.load_program(vertex_shader = "fractal.vert", fragment_shader = "julia.frag")
        julia["colorGradient"] = self.juliaGradient
        self.juliaVA = self.ctx.vertex_array(julia, self.screenVB, "in_vert")

        self.currentVA = self.mandelbrotVA
        self.update_fractal()

    def update_fractal(self):
        p = self.currentVA.program
        p["screenSize"] = self.wnd.size
        p["center"] = self.center
        p["zoom"] = self.zoom * self.wnd.size[0] / self.wnd.size[1], self.zoom
        p["limit"] = self.limit
        if self.currentVA == self.nthMandelbrotVA:
            p["power"] = self.nthMandelbrotPower
        if self.currentVA == self.juliaVA:
            p["c"] = self.juliaC

    def on_render(self, time, frameTime):
        self.currentVA.render(mgl.TRIANGLES)
        # self.nthMandelbrotVA.program["power"] = self.nthMandelbrotVA.program["power"].value + frameTime * 0.1

        # self.renderUi(time, frameTime)

    def renderUi(self, time, frameTime):
        imgui.new_frame()
        imgui.set_next_window_pos((0,0), imgui.Cond_.appearing.value)
        imgui.set_next_window_size((30,20), imgui.Cond_.appearing.value)

        imgui.begin("Settings")
        imgui.text("Bar")
        imgui.text_colored(imgui.ImVec4(0.2, 1.0, 0.0, 1.0), "Eggs")
        imgui.end()

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
            if self.currentVA == self.mandelbrotVA:
                screenRatio = self.wnd.size[0] / self.wnd.size[1]
                self.juliaC[0] = (x / self.wnd.size[0] - 0.5) * self.zoom * screenRatio + self.center[0]
                self.juliaC[1] = -(y / self.wnd.size[1] - 0.5) * self.zoom + self.center[1]
                self.currentVA = self.juliaVA
                self.zoom = 2
                self.center = [0, 0]

            elif self.currentVA == self.juliaVA:
                self.currentVA = self.mandelbrotVA
                self.zoom = 2
                self.center = [0, 0]
            
            self.update_fractal()


    def on_mouse_release_event(self, x, y, button):
        self.imgui.mouse_release_event(x, y, button)

    def on_unicode_char_entered(self, char):
        self.imgui.unicode_char_entered(char)