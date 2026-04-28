import OpenGL.GL as GL
from material.material import Material


class TextureMaterial(Material):
    def __init__(self, texture1, texture2=None, property_dict={}):
        vertex_shader_code = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;

        in vec3 vertexPosition;
        in vec2 vertexUV;
        in vec3 vertexNormal;

        uniform vec2 repeatUV;
        uniform vec2 offsetUV;

        out vec2 UV;
        out vec3 normal;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);

            UV = vertexUV * repeatUV + offsetUV;
            normal = vertexNormal;
        }
        """

        fragment_shader_code = """
        uniform vec3 baseColor;

        uniform sampler2D texture1;
        uniform sampler2D texture2;

        uniform int useTexture2;

        in vec2 UV;
        in vec3 normal;

        out vec4 fragColor;

        void main()
        {
            vec4 tex1 = texture(texture1, UV);
            vec4 tex2 = texture(texture2, UV);

            vec4 color;

            if (useTexture2 == 1)
            {
                float factor = abs(normal.y);
                color = mix(tex2, tex1, factor);
            }
            else
            {
                color = tex1;
            }

            fragColor = vec4(baseColor, 1.0) * color;
        }
        """

        super().__init__(vertex_shader_code, fragment_shader_code)

        # base color
        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])

        # texture 1 (always required)
        self.add_uniform("sampler2D", "texture1", [texture1.texture_ref, 0])

        # texture 2 (optional)
        if texture2 is not None:
            self.add_uniform("sampler2D", "texture2", [texture2.texture_ref, 1])
            self.add_uniform("int", "useTexture2", 1)
        else:
            self.add_uniform("sampler2D", "texture2", [texture1.texture_ref, 1])
            self.add_uniform("int", "useTexture2", 0)

        # UV controls
        self.add_uniform("vec2", "repeatUV", [1.0, 1.0])
        self.add_uniform("vec2", "offsetUV", [0.0, 0.0])

        self.locate_uniforms()

        # render settings
        self.setting_dict["doubleSide"] = True
        self.setting_dict["wireframe"] = False
        self.setting_dict["lineWidth"] = 1

        self.set_properties(property_dict)

    def update_render_settings(self):
        if self.setting_dict["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)

        if self.setting_dict["wireframe"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

        GL.glLineWidth(self.setting_dict["lineWidth"])