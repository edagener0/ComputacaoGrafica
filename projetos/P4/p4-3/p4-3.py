"""Animation example"""
import OpenGL.GL as GL
import math

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute
from core.uniform import Uniform


class Example(Base):
    """ Animate triangle moving across screen """
    def initialize(self):
        print("Initializing program...")
        # Initialize program #
        vs_code = """
            in vec3 position;
            in vec3 color;
            uniform vec3 translation;
            out vec3 vColor;
            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
                vColor = color;
            }
        """
        fs_code = """
            in vec3 vColor;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(vColor, 1.0);
            }
        """
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        # render settings (optional) #
        # Specify color used when clearly
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        # Set up vertex array object #
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        # Set up vertex attribute #

        segments = 60
        radius = 0.2

        position_data = []
        color_data = []

        position_data.append([0.0, 0.0, 0.0])
        color_data.append([1.0, 1.0, 0.0])

        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            position_data.append([x, y, 0.0])
            color_data.append([
                (math.cos(angle) + 1) / 2,
                (math.sin(angle) + 1) / 2,
                0.5
            ])

        self.vertex_count = len(position_data)

        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self.program_ref, 'position')

        color_attribute = Attribute('vec3', color_data)
        color_attribute.associate_variable(self.program_ref, 'color')

        # Set up uniforms #
        self.translation = Uniform('vec3', [-0.5, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')

    def update(self):
        """ Update data """
        # Increase x coordinate of translation
        self.translation.data[0] += 0.01
        # If triangle passes off-screen on the right,
        # change translation, so it reappears on the left
        if self.translation.data[0] > 1.2:
            self.translation.data[0] = -1.2
        # Render scene #
        # Reset color buffer with specified color
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)
        self.translation.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, self.vertex_count)


# Instantiate this class and run the program
Example().run()