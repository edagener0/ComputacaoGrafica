import OpenGL.GL as GL

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute
from core.input import Input
from core.uniform import Uniform

class Example(Base):
    def initialize(self):
        print("Initializing program...")

        
        vs_code = """
            in vec3 position;
            uniform vec3 translation;
            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
            }
        """

        
        fs_code = """
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(1.0, 0.4, 0.7, 1.0);
            }
        """

        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        self.input = Input()
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
        self.translation = Uniform('vec3', [0.0, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')

    def update(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)
        self.input.update()

        if self.input.isKeyPressed("left"):
            self.translation.data[0] = max(self.translation.data[0] - 0.1, -1 + 0.750)
        if self.input.isKeyPressed("right"):
            self.translation.data[0] = min(self.translation.data[0] + 0.1, 1 - 0.975)
        if self.input.isKeyPressed("up"):
            self.translation.data[1] = min(self.translation.data[1] + 0.1, 1 - 0.8)
        if self.input.isKeyPressed("down"):
            self.translation.data[1] = max(self.translation.data[1] - 0.1, -1 + 0.0125)

        self.translation.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)

Example().run()
