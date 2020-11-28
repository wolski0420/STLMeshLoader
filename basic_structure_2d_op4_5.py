import numpy


class BasicStructure2D:
    def __init__(self):
        self.vertices = []
        self.triangles = []

    def load_from_file(self, filename):
        file, faces = open(filename, "r"), []
        line = file.readline()
        while line:
            faces.append([int(x) for x in line.split()])
            line = file.readline()
        file.close()

        for points in faces:
            for i in range(0,6,2):
                vertex = (points[i], points[i+1])
                if vertex not in self.vertices:
                    self.vertices.append(vertex)

        for points in faces:
            self.triangles.append([])
            for i in range(0,6,2):
                vertex = (points[i], points[i+1])
                self.triangles[len(self.triangles)-1].append(vertex)

    def get_triangles_by_vertex(self, vertex):
        found_triangles = []
        for triangle in self.triangles:
            if vertex in triangle:
                found_triangles.append(triangle)
        return found_triangles

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

    # OP4
    # @param1 - triangle data
    # @param2 - target vertex data
    # @return - list of triangles on path
    # it works in case that mesh is not concave
    def get_triangles_path(self, triangle, target_vertex):
        curr, path = triangle, [triangle]
        while curr[0] != target_vertex and curr[1] != target_vertex and curr[2] != target_vertex:
            neighbours, min_vertex, min_triangle = self.get_triangle_neighbourhood(curr, 1), None, None
            for triangle in neighbours:
                if triangle not in path:
                    for vertex in triangle:
                        if vertex not in curr:
                            if min_vertex is None:
                                min_vertex = vertex
                                min_triangle = triangle
                            else:
                                point1 = numpy.array(vertex)
                                point2 = numpy.array(min_vertex)
                                point3 = numpy.array(target_vertex)
                                new_dist = numpy.linalg.norm(point3 - point1)
                                dist = numpy.linalg.norm(point3 - point2)
                                if new_dist < dist:
                                    min_vertex = vertex
                                    min_triangle = triangle
            curr = min_triangle
            path.append(min_triangle)
        return path

    # OP5
    # @param1 - first triangle data
    # @param2 - second triangle data
    def swap_edges(self, first, second):
        first_triangle, second_triangle = None, None
        for t in self.triangles:
            if t[0] in first and t[1] in first and t[2] in first:
                first_triangle = t
            if t[0] in second and t[1] in second and t[2] in second:
                second_triangle = t

        common_vertices, distinct_vertices = [], []

        for vertex in first_triangle:
            if vertex in second_triangle:
                common_vertices.append(vertex)
            else:
                distinct_vertices.append(vertex)

        for vertex in second_triangle:
            if vertex not in common_vertices:
                distinct_vertices.append(vertex)

        first_triangle[0], first_triangle[1], first_triangle[2] = distinct_vertices[0], common_vertices[0], distinct_vertices[1]
        second_triangle[0], second_triangle[1], second_triangle[2] = distinct_vertices[0], common_vertices[1], distinct_vertices[1]

        p1, p2, p3 = first_triangle[0], first_triangle[1], first_triangle[2]
        cross = numpy.cross([p2[0]-p1[0], p2[1]-p1[1]], [p3[0]-p2[0], p3[1]-p2[1]])
        if cross < 0:
            first_triangle.reverse()

        p1, p2, p3 = second_triangle[0], second_triangle[1], second_triangle[2]
        cross = numpy.cross([p2[0] - p1[0], p2[1] - p1[1]], [p3[0] - p2[0], p3[1] - p2[1]])
        if cross < 0:
            second_triangle.reverse()
