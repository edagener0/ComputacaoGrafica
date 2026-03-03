"""Animation example"""
import OpenGL.GL as GL
import random
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
            uniform vec3 translation;
            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
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
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        # render settings (optional) #
        # Specify color used when clearly
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        # Set up vertex array object #
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        # Set up vertex attribute #
        position_data = [[ 0.0,  0.2,  0.0],
                         [ 0.2, -0.2,  0.0],
                         [-0.2, -0.2,  0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self.program_ref, 'position')
        # Set up uniforms #
        self.translation = Uniform('vec3', [0.0, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')
        self.base_color = Uniform('vec3', [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, 'baseColor')

        angle = random.uniform(0, 2 * math.pi)
        speed = 0.02
        self.velocity = [math.cos(angle) * speed,
                         math.sin(angle) * speed]

        self.limit = 0.8
        self.max_speed = 0.03
        self.min_speed = 0.005

    def update(self):
        """ Update data """
        # Increase x coordinate of translation
        self.velocity[0] += random.uniform(-0.002, 0.002)
        self.velocity[1] += random.uniform(-0.002, 0.002)

        speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if speed > self.max_speed:
            factor = self.max_speed / speed
            self.velocity[0] *= factor
            self.velocity[1] *= factor
        elif speed < self.min_speed:
            factor = self.min_speed / speed
            self.velocity[0] *= factor
            self.velocity[1] *= factor

        self.translation.data[0] += self.velocity[0]
        self.translation.data[1] += self.velocity[1]

        # If triangle passes off-screen on the right,
        # change translation, so it reappears on the left
        if self.translation.data[0] > self.limit:
            self.translation.data[0] = self.limit
            self.velocity[0] *= -1
        elif self.translation.data[0] < -self.limit:
            self.translation.data[0] = -self.limit
            self.velocity[0] *= -1

        if self.translation.data[1] > self.limit:
            self.translation.data[1] = self.limit
            self.velocity[1] *= -1
        elif self.translation.data[1] < -self.limit:
            self.translation.data[1] = -self.limit
            self.velocity[1] *= -1

        # Render scene #
        # Reset color buffer with specified color
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)
        self.translation.upload_data()
        self.base_color.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


# Instantiate this class and run the program
Example().run()