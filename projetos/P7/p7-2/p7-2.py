from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from geometry.box import BoxGeometry
from material.surface import SurfaceMaterial
from core.input import Input


class Example(Base):
    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 4])
        self.input = Input()

        geometry = BoxGeometry()
        material = SurfaceMaterial(property_dict={"useVertexColors": True})

        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

        self.rot_speed_x = 0
        self.rot_speed_y = 0
        self.rot_speed_z = 0
        self.step = 0.001

    def update(self):
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
