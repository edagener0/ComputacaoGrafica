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