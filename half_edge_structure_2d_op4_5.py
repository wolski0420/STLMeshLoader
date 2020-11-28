import numpy


class Vertex:
    def __init__(self, half_edge, data):
        self.half_edge = half_edge
        self.data = data


class Face:
    def __init__(self, half_edge, data):
        self.half_edge = half_edge
        self.data = data


class HalfEdge:
    def __init__(self, vertex, face, next_he, prev_he, opposite):
        self.vertex = vertex
        self.face = face
        self.next_he = next_he
        self.prev_he = prev_he
        self.opposite = opposite


class HalfEdgesMesh2D:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.half_edges = []

    def load_from_file(self, filename):
        file, faces = open(filename, "r"), []
        line = file.readline()
        while line:
            faces.append([int(x) for x in line.split()])
            line = file.readline()
        file.close()

        for triangle in faces:
            points = [(triangle[i], triangle[i + 1]) for i in range(0, 6, 2)]
            new_vertices = [Vertex(None, point) for point in points]
            face = Face(None, points)

            new_half_edges = [HalfEdge(v, face, None, None, None) for v in new_vertices]
            for i in range(3):
                new_half_edges[i - 1].next_he = new_half_edges[i]
                new_half_edges[i].prev_he = new_half_edges[i - 1]
                new_vertices[i].half_edge = new_half_edges[i]

            face.half_edge = new_half_edges[0]
            self.half_edges += new_half_edges
            self.faces.append(face)
            self.vertices += new_vertices

        for he in self.half_edges:
            opp_vertex = he.next_he.vertex
            found = self.find_half_edges_by_vertex(opp_vertex)
            opposite_found = None
            for f in found:
                if f.next_he.vertex.data == he.vertex.data:
                    opposite_found = f
            he.opposite = opposite_found
            if opposite_found is not None:
                opposite_found.opposite = he

    def find_half_edges_by_vertex(self, vertex):
        data = vertex.data
        found_he = []
        for he in self.half_edges:
            if he.vertex.data == data:
                found_he.append(he)
        return found_he

    def find_face_by_triangle_data(self, triangle):
        for face in self.faces:
            if triangle[0] in face.data and triangle[1] in face.data and triangle[2] in face.data:
                return face
        return None

    def get_triangles_by_vertex(self, vertex):
        faces = []
        for he in self.half_edges:
            if vertex == he.vertex.data and he.face not in faces:
                faces.append(he.face)
        return faces

    def get_triangle_neighbourhood(self, triangle, layers_no):
        neighbourhood, end_of_nbh = [self.find_face_by_triangle_data(triangle)], 0
        for i in range(layers_no):
            new_nbh = []
            for j in range(end_of_nbh, len(neighbourhood)):
                he1 = neighbourhood[j].half_edge
                he2, he3 = he1.next_he.opposite, he1.prev_he.opposite
                he1 = he1.opposite
                if he1 is not None and he1.face not in neighbourhood and he1.face not in new_nbh:
                    new_nbh.append(he1.face)
                if he2 is not None and he2.face not in neighbourhood and he2.face not in new_nbh:
                    new_nbh.append(he2.face)
                if he3 is not None and he3.face not in neighbourhood and he3.face not in new_nbh:
                    new_nbh.append(he3.face)
            neighbourhood += new_nbh
            end_of_nbh = len(neighbourhood) - len(new_nbh)
        return [face.data for face in neighbourhood[1:]]

    # OP4
    # @param1 - triangle data
    # @param2 - target vertex
    # @return - list of triangles on path
    # it works in case that mesh is not concave
    def get_triangles_path(self, triangle, target):
        curr = self.find_face_by_triangle_data(triangle)
        path, first_he = [curr], curr.half_edge
        second_he, third_he = first_he.next_he, first_he.prev_he

        while first_he.vertex.data != target and second_he.vertex.data != target and third_he.vertex.data != target:
            ngh_he = [first_he.opposite, second_he.opposite, third_he.opposite]
            min_he = None
            for he in ngh_he:
                if he is not None:
                    if min_he is None:
                        min_he = he
                    else:
                        new_dist = numpy.linalg.norm(numpy.array(he.prev_he.vertex.data) - numpy.array(target))
                        dist = numpy.linalg.norm(numpy.array(min_he.prev_he.vertex.data) - numpy.array(target))
                        if new_dist < dist:
                            min_he = he
            path.append(min_he.face)
            curr = min_he.face
            first_he = curr.half_edge
            second_he, third_he = first_he.next_he, first_he.prev_he
        return [triangle.data for triangle in path]

    # OP5
    # @param1 - first triangle data
    # @param2 - second triangle data
    def swap_edges(self, first, second):
        first_triangle = self.find_face_by_triangle_data(first)
        second_triangle = self.find_face_by_triangle_data(second)

        fst_common_he, snd_common_he = None, None
        first_iter, second_iter = first_triangle.half_edge, second_triangle.half_edge
        while fst_common_he is None and snd_common_he is None:
            for i in range(3):
                if first_iter.opposite == second_iter:
                    fst_common_he = first_iter
                    snd_common_he = second_iter
                    break
                else:
                    second_iter = second_iter.next_he

            if fst_common_he is not None and snd_common_he is not None:
                break
            first_iter = first_iter.next_he

        fst_prev_he, fst_next_he = fst_common_he.prev_he, fst_common_he.next_he
        snd_prev_he, snd_next_he = snd_common_he.prev_he, snd_common_he.next_he

        fst_prev_he.next_he = snd_next_he
        snd_next_he.prev_he = fst_prev_he
        fst_prev_he.prev_he = fst_common_he
        fst_common_he.next_he = fst_prev_he
        snd_next_he.next_he = fst_common_he
        fst_common_he.prev_he = snd_next_he

        snd_prev_he.next_he = fst_next_he
        fst_next_he.prev_he = snd_prev_he
        snd_prev_he.prev_he = snd_common_he
        snd_common_he.next_he = snd_prev_he
        fst_next_he.next_he = snd_common_he
        snd_common_he.prev_he = fst_next_he

        fst_common_he.vertex.data = snd_prev_he.vertex.data
        snd_common_he.vertex.data = fst_prev_he.vertex.data

        snd_next_he.face = fst_prev_he.face
        fst_next_he.face = snd_prev_he.face

        fst_prev_he.face.half_edge = fst_prev_he
        snd_prev_he.face.half_edge = snd_prev_he

        fst_prev_he.face.data = [fst_prev_he.vertex.data, snd_next_he.vertex.data, fst_common_he.vertex.data]
        snd_prev_he.face.data = [snd_prev_he.vertex.data, fst_next_he.vertex.data, snd_common_he.vertex.data]
