"""An example of a regular pentagon :) """

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from geometry.polygon import PolygonGeometry
from material.point import PointMaterial
from material.surface import SurfaceMaterial


class Example(Base):
    """ Render a regular polygon"""
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 4])
        geometry = PolygonGeometry(5)
        # material = PointMaterial(property_dict={"baseColor": [1, 1, 0], "pointSize": 5})
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        # material = SurfaceMaterial(
        #     property_dict= {
        #         "useVertexColors": True,
        #         "wireframe": True,
        #         "lineWidth": 8
        #     }
        # )
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        """Updating scene with movement"""
        self.mesh.rotate_z(0.01337)
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()