import numpy as np
import math
import pathlib
import sys

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from extras.axes import AxesHelper
from extras.grid import GridHelper
from extras.movement_rig import MovementRig
from geometry.tau import TauGeometry
from core.input import Input
from material.surface import SurfaceMaterial

class Example(Base):
    """
    Render the axes and the rotated xy-grid.
    Add camera movement: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
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

        self.input = Input()
        geometry = TauGeometry()
        material = SurfaceMaterial(property_dict={"useVertexColors": True, "doubleSide": True})
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)
        self.step = 0.001
        self.rot_speed_x = 0
        self.rot_speed_y = 0
        self.rot_speed_z = 0

        print("""
                CONTROLOS

        Câmara
        W / S : mover para frente / trás
        A / D : mover para esquerda / direita
        R / F : mover para cima / baixo
        Q / E : girar à esquerda / direita
        T / G : olhar para cima / baixo

        Tau
        I / K : mover objeto para frente / trás
        J / L : mover objeto para esquerda / direita
        U / O : mover objeto para cima / baixo

        Rotação do objeto
        X : aumentar rotação eixo X
        Y : aumentar rotação eixo Y
        Z : aumentar rotação eixo Z
        S : desacelerar rotação
        SPACE : parar rotação
        C : inverter direção da rotação
        """)


    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)

        move_speed = 2 * self.delta_time

        if self.input.is_key_pressed("i"):
            self.mesh.translate(0, 0, -move_speed)

        if self.input.is_key_pressed("k"):
            self.mesh.translate(0, 0, move_speed)

        if self.input.is_key_pressed("j"):
            self.mesh.translate(-move_speed, 0, 0)

        if self.input.is_key_pressed("l"):
            self.mesh.translate(move_speed, 0, 0)

        if self.input.is_key_pressed("u"):
            self.mesh.translate(0, move_speed, 0)

        if self.input.is_key_pressed("o"):
            self.mesh.translate(0, -move_speed, 0)

        if self.input.is_key_pressed("x"):
            self.rot_speed_x += self.step

        if self.input.is_key_pressed("y"):
            self.rot_speed_y += self.step

        if self.input.is_key_pressed("z"):
            self.rot_speed_z += self.step

        if self.input.is_key_pressed("s"):
            self.rot_speed_x *= 0.95
            self.rot_speed_y *= 0.95
            self.rot_speed_z *= 0.95

        if self.input.is_key_down("space"):
            self.rot_speed_x = 0
            self.rot_speed_y = 0
            self.rot_speed_z = 0

        if self.input.is_key_down("c"):
            self.rot_speed_x *= -1
            self.rot_speed_y *= -1
            self.rot_speed_z *= -1

        self.mesh.rotate_x(self.rot_speed_x)
        self.mesh.rotate_y(self.rot_speed_y)
        self.mesh.rotate_z(self.rot_speed_z)

        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
