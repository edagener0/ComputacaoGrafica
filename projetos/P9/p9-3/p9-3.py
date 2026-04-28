import numpy as np
import math
import pathlib
import sys

from core.obj_reader import my_obj_reader
import random
from geometry.geometry import Geometry
from material.surface import SurfaceMaterial


from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from extras.axes import AxesHelper
from extras.grid import GridHelper
from extras.movement_rig import MovementRig

from material.texture import TextureMaterial
from core_ext.texture import Texture


class Example(Base):
    """
    Render the axes and the rotated xy-grid.
    Add camera movement: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600) # type: ignore
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0.5, 1, 5])
        self.scene.add(self.rig)
        axes = AxesHelper(axis_length=2)
        self.scene.add(axes)
        grid = GridHelper(
            size=20,
            grid_color=[1, 1, 1],
            center_color=[1, 1, 0]
        )
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        position_data = my_obj_reader("./core/letra.obj")

        geometry = Geometry()

        # -------------------------
        # UVs (ADICIONA AQUI)
        # -------------------------
        x_values = [pos[0] for pos in position_data]
        z_values = [pos[2] for pos in position_data]

        x_min, x_max = min(x_values), max(x_values)
        z_min, z_max = min(z_values), max(z_values)

        uv_data = []

        for pos in position_data:
            u = (pos[0] - x_min) / (x_max - x_min)
            v = (pos[2] - z_min) / (z_max - z_min)
            uv_data.append([u, v])

        geometry.add_attribute("vec2", "vertexUV", uv_data)

        # -------------------------
        # CORES (o teu código)
        # -------------------------
        y_values = [pos[1] for pos in position_data]
        y_min = min(y_values)
        y_max = max(y_values)

        color_data = []

        for pos in position_data:
            y = pos[1]

            t = (y - y_min) / (y_max - y_min)

            color = [
                t,
                0.2,
                1.0 - t
            ]

            color_data.append(color)

        geometry.add_attribute("vec3", "vertexColor", color_data)

        # posição SEMPRE no fim ou depois
        geometry.add_attribute("vec3", "vertexPosition", position_data)

        # -------------------------
        # NORMAIS (FIXED)
        # -------------------------
        normal_data = []

        threshold = y_min + (y_max - y_min) * 0.9  # top 10%

        for pos in position_data:
            if pos[1] >= threshold:
                normal = [0, 1, 0]   # topo
            else:
                normal = [0, 0, 1]   # lados (melhor que [1,0,0])
            normal_data.append(normal)

        geometry.add_attribute("vec3", "vertexNormal", normal_data)

        geometry.count_vertices()

        img_texture1 = Texture(file_name="./images/grass.jpg")
        img_texture2 = Texture(file_name="./images/crate.jpg")

        material = TextureMaterial(texture1=img_texture1, texture2=img_texture2)
        # TILING (repeat texture)
        material.uniform_dict["repeatUV"].data = [4.0, 4.0]

        # OFFSET (optional stretch/move)
        material.uniform_dict["offsetUV"].data = [0.0, 0.0]
        self.mesh = Mesh(geometry, material)

        self.mesh.set_position([0, 0, 0])

        self.scene.add(self.mesh)
        self.rot_speed = [0.0, 0.0, 0.0]


    def update(self):
        step = 0.005

        if self.input.is_key_pressed("x"):
            self.rot_speed[0] += step

        if self.input.is_key_pressed("y"):
            self.rot_speed[1] += step

        if self.input.is_key_pressed("z"):
            self.rot_speed[2] += step

        if self.input.is_key_pressed("X"):
            self.rot_speed[0] -= step

        if self.input.is_key_pressed("Y"):
            self.rot_speed[1] -= step

        if self.input.is_key_pressed("Z"):
            self.rot_speed[2] -= step

        if self.input.is_key_pressed("s"):
            self.rot_speed = [v * 0.5 for v in self.rot_speed]

        if self.input.is_key_down("space"):
            self.rot_speed = [0.0, 0.0, 0.0]

        if self.input.is_key_down("r"):
            self.rot_speed[0] *= -1
            self.rot_speed[1] *= -1
            self.rot_speed[2] *= -1

        self.mesh.rotate_x(self.rot_speed[0])
        self.mesh.rotate_y(self.rot_speed[1])
        self.mesh.rotate_z(self.rot_speed[2])

        self.renderer.render(self.scene, self.camera)
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)

print(
    "camara:\n"
    "w - move forwards\n"
    "s - move backwards\n"
    "move left = a\n"
    "move right = d\n"
    "move up = r\n"
    "move down = f\n"
    "turn left = q\n"
    "turn right = e\n"
    "look up = t\n"
    "look down = g"
    "\n\n"
    "objeto:\n"
    "x - aumenta a velocidade no eixo x\n"
    "y - aumenta a velocidade no eixo y\n"
    "z - aumenta a velocidade no eixo z\n"
    "r - inverte as rotacoes\n"
    "space - para tudo\n"
    "s - diminui as velocidade\n"
)

# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()