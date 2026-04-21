import math

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
from core_ext.texture import Texture
from material.multitexture import MultiTextureMaterial


class Example(Base):

    def initialize(self):
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

        grass = Texture(file_name="images/grass.jpg")
        sky = Texture(file_name="images/sky.jpg")

        material = MultiTextureMaterial(grass, sky)

        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


Example(screen_size=[800, 600]).run()