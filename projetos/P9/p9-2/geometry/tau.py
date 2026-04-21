from geometry.geometry import Geometry


class TauGeometry(Geometry):
    def __init__(self):
        super().__init__()

        w = 1.5
        h = 1.6
        t = 0.5
        d = 0.3

        p0 = [-t/2, -h/2,  d/2]
        p1 = [ t/2, -h/2,  d/2]
        p2 = [-t/2,  h/2,  d/2]
        p3 = [ t/2,  h/2,  d/2]

        p0b = [-t/2, -h/2, -d/2]
        p1b = [ t/2, -h/2, -d/2]
        p2b = [-t/2,  h/2, -d/2]
        p3b = [ t/2,  h/2, -d/2]

        p4 = [-w/2,  h/2,  d/2]
        p5 = [ w/2,  h/2,  d/2]
        p6 = [-w/2,  h/2 + t, d/2]
        p7 = [ w/2,  h/2 + t, d/2]

        p4b = [-w/2,  h/2,  -d/2]
        p5b = [ w/2,  h/2,  -d/2]
        p6b = [-w/2,  h/2 + t, -d/2]
        p7b = [ w/2,  h/2 + t, -d/2]

        position_data = [

            p0, p1, p3,  p0, p3, p2,
            p1b, p0b, p2b,  p1b, p2b, p3b,
            p0, p2, p2b,  p0, p2b, p0b,
            p1, p3, p3b,  p1, p3b, p1b,
            p0, p1, p1b,  p0, p1b, p0b,
            p2, p3, p3b,  p2, p3b, p2b,

            p4, p5, p7,  p4, p7, p6,
            p5b, p4b, p6b,  p5b, p6b, p7b,
            p4, p6, p6b,  p4, p6b, p4b,
            p5, p7, p7b,  p5, p7b, p5b,
            p4, p5, p5b,  p4, p5b, p4b,
            p6, p7, p7b,  p6, p7b, p6b,

            p2, p3, p5,  p2, p5, p4,
            p2b, p3b, p5b,  p2b, p5b, p4b,
        ]

        uv_pattern = [
            [0, 0],
            [1, 0],
            [0.5, 1]
        ]

        uv_data = []

        for i in range(len(position_data)):
            uv_data.append(uv_pattern[i % 3])

        
        color_data = []

        for i in range(len(position_data)):
            if i < len(position_data) // 2:
                color_data.append([1.0, 0.0, 0.0])  
            else:
                color_data.append([0.0, 0.0, 0.0])  

        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        
        self.add_attribute("vec3", "vertexColor", color_data)

        self.count_vertices()