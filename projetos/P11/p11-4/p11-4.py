import numpy as np
import math

from core.obj_reader import my_obj_reader
from geometry.geometry import Geometry

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from extras.axes import AxesHelper
from extras.grid import GridHelper
from extras.movement_rig import MovementRig
from geometry.sphere import SphereGeometry
from geometry.rectangle import RectangleGeometry
from material.texture import TextureMaterial
from core_ext.texture import Texture


class Example(Base):
    def initialize(self):
        print("Initializing program...")

        self.renderer = Renderer()
        self.scene = Scene()

        self.camera = Camera(aspect_ratio=800 / 600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0.5, 1, 5])
        self.scene.add(self.rig)

        axes = AxesHelper(axis_length=2)
        self.scene.add(axes)

        grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        sky_geometry = SphereGeometry(radius=50)
        sky_material = TextureMaterial(
            texture1=Texture(file_name="./images/sky.jpg")
        )
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)

        grass_geometry = RectangleGeometry(width=100, height=100)
        grass_material = TextureMaterial(
            texture1=Texture(file_name="./images/grass.jpg")
        )
        grass_material.uniform_dict["repeatUV"].data = [50.0, 50.0]

        grass = Mesh(grass_geometry, grass_material)
        grass.rotate_x(-math.pi / 2)
        self.scene.add(grass)
        
        self.group = MovementRig()
        self.scene.add(self.group)

        
        tex1 = Texture(file_name="./images/rgb-noise.jpg")
        tex2 = Texture(file_name="./images/crate.jpg")

        material = TextureMaterial(texture1=tex1, texture2=tex2)
        material.uniform_dict["repeatUV"].data = [4.0, 4.0]

        
        def create_letter(path):
            position_data = my_obj_reader(path)
            geometry = Geometry()

            
            x_vals = [p[0] for p in position_data]
            z_vals = [p[2] for p in position_data]
            x_min, x_max = min(x_vals), max(x_vals)
            z_min, z_max = min(z_vals), max(z_vals)

            uv_data = []
            for p in position_data:
                u = (p[0] - x_min) / (x_max - x_min)
                v = (p[2] - z_min) / (z_max - z_min)
                uv_data.append([u, v])

            geometry.add_attribute("vec2", "vertexUV", uv_data)

            
            geometry.add_attribute("vec3", "vertexPosition", position_data)

            
            y_vals = [p[1] for p in position_data]
            y_min, y_max = min(y_vals), max(y_vals)
            threshold = y_min + (y_max - y_min) * 0.9

            normals = []
            for p in position_data:
                if p[1] >= threshold:
                    normals.append([0, 1, 0])
                else:
                    normals.append([0, 0, 1])

            geometry.add_attribute("vec3", "vertexNormal", normals)

            geometry.count_vertices()

            return Mesh(geometry, material)

        
        self.mesh1 = create_letter("./core/letra.obj")
        self.mesh2 = create_letter("./core/letra_david.obj")

        
        self.mesh1.set_position([-1.5, 0, 0])
        self.mesh2.set_position([1.5, 0, 0])

        
        self.group.add(self.mesh1)
        self.group.add(self.mesh2)

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

        
        self.mesh1.rotate_x(self.rot_speed[0])
        self.mesh1.rotate_y(self.rot_speed[1])
        self.mesh1.rotate_z(self.rot_speed[2])

        self.mesh2.rotate_x(self.rot_speed[0])
        self.mesh2.rotate_y(self.rot_speed[1])
        self.mesh2.rotate_z(self.rot_speed[2])

        self.renderer.render(self.scene, self.camera)
        self.rig.update(self.input, self.delta_time)

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
Example(screen_size=[800, 600]).run()