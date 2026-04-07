""" Render the sine function with progressive wave motion """
import numpy as np

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from geometry.geometry import Geometry
from material.point import PointMaterial
from material.line import LineMaterial


class Example(Base):
    """ Render a moving sine wave """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 5])

        self.geometry = Geometry()

        # shaders
        vs_code = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
        }
        """

        fs_code = """
        uniform vec3 baseColor;
        uniform bool useVertexColors;
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(baseColor, 1.0);
        }
        """

        self.x_values = np.arange(-3.2, 3.2, 0.2)

        self.position_data = [[x, np.sin(x), 0] for x in self.x_values]

        self.geometry.add_attribute("vec3", "vertexPosition", self.position_data)
        self.geometry.count_vertices()

        use_vertex_colors = False

        point_material = PointMaterial(
            vs_code,
            fs_code,
            {"baseColor": [1, 1, 1], "pointSize": 10},
            use_vertex_colors
        )
        self.point_mesh = Mesh(self.geometry, point_material)


        line_material = LineMaterial(
            vs_code,
            fs_code,
            {"baseColor": [1, 0, 0], "lineWidth": 2},
            use_vertex_colors
        )
        self.line_mesh = Mesh(self.geometry, line_material)

        self.scene.add(self.point_mesh)
        self.scene.add(self.line_mesh)

    def update(self):
        time = self.time

        # nova onda
        position_data = [[x, np.sin(x - time), 0] for x in self.x_values]

        # remover meshes antigos
        self.scene.remove(self.point_mesh)
        self.scene.remove(self.line_mesh)

        # criar nova geometria
        geometry = Geometry()
        geometry.add_attribute("vec3", "vertexPosition", position_data)
        geometry.count_vertices()

        # recriar meshes (IMPORTANTE!)
        point_material = self.point_mesh.material
        line_material = self.line_mesh.material

        self.point_mesh = Mesh(geometry, point_material)
        self.line_mesh = Mesh(geometry, line_material)

        # adicionar novamente à cena
        self.scene.add(self.point_mesh)
        self.scene.add(self.line_mesh)

        # render
        self.renderer.render(self.scene, self.camera)


# run
Example(screen_size=[800, 600]).run()