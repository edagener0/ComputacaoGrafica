import OpenGL.GL as GL

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute


class Example(Base):
    def initialize(self):
        print("Initializing program...")

        
        vs_code = """
            in vec3 position;
            in vec3 vertexColor;
            out vec3 color;
            void main()
            {
                gl_Position = vec4(position.x, position.y, position.z, 1.0);
                color = vertexColor;
            }
        """

        
        fs_code = """
            in vec3 color;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(color, 1.0);
            }
        """

        self.program_ref = Utils.initialize_program(vs_code, fs_code)

        
        GL.glLineWidth(7)
        GL.glPointSize(15)
        
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)

        
        position_data = [
            [ 0.8,  0.0,  0.0],
            [ 0.4,  0.6,  0.0],
            [-0.4,  0.6,  0.0],
            [-0.8,  0.0,  0.0],
            [-0.4, -0.6,  0.0],
            [ 0.4, -0.6,  0.0]
        ]

        
        color_data = [
            [1.0, 0.0, 0.0],  
            [0.0, 1.0, 0.0],  
            [0.0, 0.0, 1.0],  
            [1.0, 1.0, 0.0],  
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0],
        ]

        self.vertex_count = len(position_data)

        
        position_attribute = Attribute("vec3", position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        
        color_attribute = Attribute("vec3", color_data)
        color_attribute.associate_variable(self.program_ref, "vertexColor")

    def update(self):
        GL.glUseProgram(self.program_ref)
        
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, self.vertex_count)
        
        GL.glDrawArrays(GL.GL_POINTS, 0, self.vertex_count)
        
        GL.glDrawArrays(GL.GL_LINE_LOOP, 0, self.vertex_count)


Example().run()
