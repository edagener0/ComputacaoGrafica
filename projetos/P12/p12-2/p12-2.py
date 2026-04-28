#!/usr/bin/python3
import math

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core_ext.texture import Texture

from extras.movement_rig import MovementRig

from geometry.box import BoxGeometry
from geometry.sphere import SphereGeometry

from light.directional import DirectionalLight
from light.ambient import AmbientLight

from material.phong import PhongMaterial
from material.texture import TextureMaterial


class Example(Base):

    def initialize(self):
        print("Initializing program...")

        # =========================
        # ENGINE
        # =========================
        self.renderer = Renderer()
        self.scene = Scene()

        # =========================
        # CAMERA
        # =========================
        self.camera = Camera(aspect_ratio=800 / 600)

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 2, 6])
        self.scene.add(self.rig)

        # =========================
        # LIGHTS
        # =========================
        ambient = AmbientLight(color=[0.25, 0.25, 0.25])
        self.scene.add(ambient)

        self.sun = DirectionalLight(
            color=[1.0, 1.0, 0.95],
            direction=[-0.2, -1.0, -0.9]
        )
        self.sun.set_position([5, 15, 5])

        self.scene.add(self.sun)

        self.renderer.enable_shadows(self.sun)

        # =========================
        # 🌞 SUN (FIXO + AMARELO)
        # =========================
        sun_geo = SphereGeometry(radius=0.5)

        sun_mat = PhongMaterial(
            texture=Texture("./images/crate.jpg"),
            number_of_light_sources=0,
            use_shadow=False
        )

        

        self.sun_mesh = Mesh(sun_geo, sun_mat)
        self.sun_mesh.set_position([10, 15, 10])
        self.scene.add(self.sun_mesh)

        # =========================
        # SKY
        # =========================
        sky_geo = SphereGeometry(radius=60)

        sky_mat = TextureMaterial(
            texture1=Texture("./images/sky.jpg")
        )

        sky = Mesh(sky_geo, sky_mat)
        self.scene.add(sky)

        # =========================
        # GROUND
        # =========================
        grass_geo = BoxGeometry(width=100, height=1, depth=100)

        grass_mat = PhongMaterial(
            texture=Texture("./images/grass.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        grass = Mesh(grass_geo, grass_mat)
        grass.set_position([0, -0.5, 0])
        self.scene.add(grass)

        # =========================
        # CRATE
        # =========================
        crate_geo = BoxGeometry(width=2, height=2, depth=2)

        crate_mat = PhongMaterial(
            texture=Texture("./images/crate.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        crate = Mesh(crate_geo, crate_mat)
        crate.set_position([-2, 1, 0])
        self.scene.add(crate)

        # =========================
        # BRICK WALL (SHADOW FIXED)
        # =========================
        wall_geo = BoxGeometry(width=10, height=6, depth=0.5)

        wall_mat = PhongMaterial(
            texture=Texture("./images/brick-wall.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        wall = Mesh(wall_geo, wall_mat)
        wall.set_position([0, 3, -8])
        self.scene.add(wall)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


Example(screen_size=[800, 600]).run()