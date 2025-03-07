from pathlib import Path
import moderngl as mgl
import moderngl_window as mglw
import numpy as np

class Window(mglw.WindowConfig):
    shaderDir = (Path(__file__) / "../../shaders").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.load_program(self.shaderDir / "mandelbrot.glsl")

        pos = np.mgrid[-1:1:self.window_size[0]*1j, -1:1:self.window_size[1]*1j].reshape(2,-1).astype("f4").T
        c = np.mgrid[-2:2:self.window_size[0]*1j, -2:2:self.window_size[1]*1j].reshape(2,-1).astype("f4").T

        vertices = np.concatenate([pos, c], axis=1)

        self.vbo = self.ctx.buffer(vertices.astype("f4").tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, "in_pos", "in_c")
        self.vao.program["limit"] = 25

        self.fbo = self.ctx.simple_framebuffer(self.window_size)
        self.fbo.use()

    def on_render(self, time, frame_time):
        self.fbo.clear(0, 0, 0, 1.0)
        self.vao.render(mgl.POINTS)


if __name__ == "__main__":
    zoom = 1 / 150
    center = np.complex64(0, 0)
    limit = 25
    fData, renderData = None, None

    Window.run()