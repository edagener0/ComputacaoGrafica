import OpenGL.GL as GL

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute
from core.uniform import Uniform
import math

class Example(Base):
    def initialize(self):
        print("Initializing program...")

        
        vs_code = """
            in vec3 position;
            void main()
            {
                gl_Position = vec4(position, 1.0);
            }
        """

        
        fs_code = """
            uniform vec3 baseColor;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
            }
        """
        self.jump_interval = 1
        self.last_jump_time = 0.0
        self.disappear = False
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)

        vertices = [
            [-0.8, 0.6, 0.0],   
            [ 0.8, 0.6, 0.0],   
            [ 1.0, 0.8, 0.0],   

            [-0.8, 0.6, 0.0],   
            [ 1.0, 0.8, 0.0],   
            [-0.4, 0.8, 0.0],   
            
            [-0.1, 0.0, 0.0],
            [ 0.1, 0.0, 0.0],
            [ 0.3, 0.6, 0.0],

            [-0.1, 0.0, 0.0],
            [ 0.3, 0.6, 0.0],
            [ 0.1, 0.6, 0.0], 
        ]

        self.vertex_count = len(vertices)

        position_attribute = Attribute("vec3", vertices)
        position_attribute.associate_variable(self.program_ref, "position")
        self.base_color = Uniform('vec3', [1.0, 0.4, 0.7])
        self.base_color.locate_variable(self.program_ref, 'baseColor')

    def update(self):
        if not self.disappear:
            self.base_color.data[0] = (math.sin(self.time) + 1) / 2
            self.base_color.data[1] = (math.sin(self.time + 2.1) + 1) / 2
            self.base_color.data[2] = (math.sin(self.time + 4.2) + 1) / 2
        
        if self.time - self.last_jump_time > self.jump_interval:
            self.last_jump_time = self.time
            self.disappear = not self.disappear
            if self.disappear:
                self.base_color.data[0] = 0
                self.base_color.data[1] = 0
                self.base_color.data[2] = 0

        GL.glUseProgram(self.program_ref)
        self.base_color.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


Example().run()
