"""An example of a basic scene: spinning cube"""

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from geometry.tau import TauGeometry
from material.surface import SurfaceMaterial
from material.point import PointMaterial
from core.input import Input


class Example(Base):
    """ Render a basic scene that consists of a spinning cube """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 4])
        self.input = Input()
        geometry = TauGeometry()
        # material = PointMaterial(property_dict={"baseColor": [1, 1, 0], "pointSize": 5})
        material = SurfaceMaterial(property_dict={"useVertexColors": True, "doubleSide": True})
        # material = SurfaceMaterial(
        #     property_dict= {
        #         "useVertexColors": True,
        #         "wireframe": True,
        #         "lineWidth": 8
        #     }
        # )
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
