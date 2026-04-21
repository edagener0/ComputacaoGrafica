from .material import Material


class MultiTextureMaterial(Material):
    def __init__(self, grass_texture, sky_texture):

        vertex_shader = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;

        in vec3 vertexPosition;
        in vec2 vertexUV;

        out vec2 UV;
        out float height;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);

            UV = vertexUV;

            height = vertexPosition.y;
        }
        """

        fragment_shader = """
        uniform sampler2D texture1;
        uniform sampler2D texture2;

        in vec2 UV;
        in float height;

        out vec4 fragColor;

        void main()
        {
            vec4 grass = texture(texture1, UV);
            vec4 sky = texture(texture2, UV);

            float m = smoothstep(-0.8, 2.1, height);

            fragColor = mix(grass, sky, m);
        }
        """

        super().__init__(vertex_shader, fragment_shader)

        self.add_uniform("sampler2D", "texture1", [grass_texture.texture_ref, 0])
        self.add_uniform("sampler2D", "texture2", [sky_texture.texture_ref, 1])

        self.locate_uniforms()