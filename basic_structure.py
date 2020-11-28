class BasicStructure:
    def __init__(self):
        self.vertices = []
        self.triangles = []

    def load_from_file(self, given_mesh):
        for points in given_mesh.points:
            for i in range(0, 9, 3):
                vertex = (float(points[i]), float(points[i + 1]), float(points[i + 2]))
                if vertex not in self.vertices:
                    self.vertices.append(vertex)

        for points in given_mesh.points:
            self.triangles.append([])
            for i in range(0, 9, 3):
                vertex = (points[i], points[i+1], points[i+2])
                self.triangles[len(self.triangles) - 1].append(vertex)

    # OP1
    # @param - vertex data
    # @return - list of triangles
    def get_triangles_by_vertex(self, vertex):
        found_triangles = []
        for triangle in self.triangles:
            if vertex in triangle:
                found_triangles.append(triangle)
        return found_triangles

    # OP2
    # @param1 - vertex data
    # @param2 - number of layers
    # @return - list of vertices
    def get_vertex_neighbourhood(self, vertex, layers_no):
        neighbourhood, end_of_nbh = [vertex], 0
        for i in range(layers_no):
            new_nbh = []
            for j in range(end_of_nbh, len(neighbourhood)):
                found_triangles = self.get_triangles_by_vertex(neighbourhood[j])
                for triangle in found_triangles:
                    for v in triangle:
                        if v not in neighbourhood and v not in new_nbh:
                            new_nbh.append(v)
            neighbourhood += new_nbh
            end_of_nbh = len(neighbourhood) - len(new_nbh)
        return neighbourhood[1:]

    # OP3
    # @param1 - triangle data
    # @param2 - number of layers
    # @return - list of triangles
    def get_triangle_neighbourhood(self, triangle, layers_no):
        neighbourhood, end_of_nbh = [], 0
        for t in self.triangles:
            if triangle[0] in t and triangle[1] in t and triangle[2] in t:
                neighbourhood.append(t)
                break

        for i in range(layers_no):
            new_nbh = []
            for j in range(end_of_nbh, len(neighbourhood)):
                curr_triangle = neighbourhood[j]
                elements1 = self.get_triangles_by_vertex(curr_triangle[0])
                elements2 = self.get_triangles_by_vertex(curr_triangle[1])
                elements3 = self.get_triangles_by_vertex(curr_triangle[2])
                common12, common13, common23 = [], [], []
                for element in elements1:
                    if element in elements2:
                        common12.append(element)
                for element in elements2:
                    if element in elements3:
                        common23.append(element)
                for element in elements1:
                    if element in elements3:
                        common13.append(element)
                common12.remove(neighbourhood[j])
                common13.remove(neighbourhood[j])
                common23.remove(neighbourhood[j])
                found_triangles = common12 + common13 + common23
                for t in found_triangles:
                    if t not in neighbourhood and t not in new_nbh:
                        new_nbh.append(t)
            neighbourhood += new_nbh
            end_of_nbh = len(neighbourhood) - len(new_nbh)
        return neighbourhood[1:]
