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


class HalfEdgesMesh:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.half_edges = []

    def load_from_file(self, given_mesh):
        for triangle in given_mesh:
            points = [(float(triangle[i]), float(triangle[i+1]), float(triangle[i+2])) for i in range(0, 9, 3)]
            new_vertices = [Vertex(None, point) for point in points]
            face = Face(None, points)

            new_half_edges = [HalfEdge(v, face, None, None, None) for v in new_vertices]
            for i in range(3):
                new_half_edges[i-1].next_he = new_half_edges[i]
                new_half_edges[i].prev_he = new_half_edges[i-1]
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

    # OP1
    # @param - vertex data
    # @return - list of triangles (faces)
    def get_triangles_by_vertex(self, vertex):
        faces = []
        for he in self.half_edges:
            if vertex == he.vertex.data and he.face not in faces:
                faces.append(he.face.data)
        return faces

    # OP2
    # @param1 - vertex data
    # @param2 - number of layers
    # @return - list of vertices
    def get_vertex_neighbourhood(self, vertex, layers_no):
        neighbourhood, end_of_nbh, result = [], 0, []
        for v in self.vertices:
            if v.data == vertex:
                neighbourhood.append(v)
                break

        for i in range(layers_no):
            new_nbh = []
            for j in range(end_of_nbh, len(neighbourhood)):
                prev_curr = neighbourhood[j].half_edge.prev_he
                next_curr = neighbourhood[j].half_edge
                while prev_curr is not None and next_curr is not None:
                    if prev_curr.vertex.data not in result and prev_curr.vertex.data != vertex:
                        new_nbh.append(prev_curr.vertex)
                        result.append(prev_curr.vertex.data)
                    if next_curr.next_he.vertex.data not in result and next_curr.next_he.vertex.data != vertex:
                        new_nbh.append(next_curr.next_he.vertex)
                        result.append(next_curr.next_he.vertex.data)
                    prev_curr, next_curr = prev_curr.opposite, next_curr.opposite
                    if prev_curr is not None:
                        prev_curr = prev_curr.prev_he
                    if next_curr is not None:
                        next_curr = next_curr.next_he
                    if prev_curr.next_he == next_curr:
                        break

                if prev_curr.next_he != next_curr:
                    while prev_curr is not None:
                        if prev_curr.vertex.data not in result and prev_curr.vertex.data != vertex:
                            new_nbh.append(prev_curr.vertex)
                            result.append(prev_curr.vertex.data)
                        prev_curr = prev_curr.opposite
                        if prev_curr is not None:
                            prev_curr = prev_curr.prev_he

                    while next_curr is not None:
                        if next_curr.next_he.vertex.data not in result and next_curr.next_he.vertex.data != vertex:
                            new_nbh.append(next_curr.next_he.vertex)
                            result.append(next_curr.next_he.vertex.data)
                        next_curr = next_curr.opposite
                        if next_curr is not None:
                            next_curr = next_curr.next_he
            neighbourhood += new_nbh
            end_of_nbh = len(neighbourhood) - len(new_nbh)
        return result

    # OP3
    # @param1 - triangle data
    # @param2 - number of layers
    # @return - list of triangles
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
