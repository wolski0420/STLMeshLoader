from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from basic_structure import BasicStructure
from basic_structure_2d_op4_5 import BasicStructure2D
from half_edge_structure import HalfEdgesMesh
from half_edge_structure_2d_op4_5 import HalfEdgesMesh2D
from time import time


def example_test():
    file_mesh = mesh.Mesh.from_file('examples/cube2.stl')

    # (A) structure with half edges (only op1-3)

    hem_example = HalfEdgesMesh()
    hem_example.load_from_file(file_mesh)
    print("(A) HalfEdge Structure :: all half edges")
    for he in hem_example.half_edges:
        print("(A) HalfEdge Structure :: vertex and face data of single half edge")
        print(he.vertex.data)
        print(he.face.data)
    print("(A) HalfEdge Structure :: OP1 - get_triangles_by_vertex")
    for face in hem_example.get_triangles_by_vertex((0.0, 0.0, 0.0)):
        print(face)
    print("(A) HalfEdge Structure :: OP2 - get_vertex_neighbourhood")
    print(hem_example.get_vertex_neighbourhood((0.0, 0.0, 0.0), 1))
    print("(A) HalfEdge Structure :: OP3 - get_triangle_neighbourhood")
    for triangle in hem_example.get_triangle_neighbourhood([(0.0, 30.0, 0.0), (0.0, 0.0, 30.0), (0.0, 30.0, 30.0)], 2):
        print(triangle)

    hem2_example = HalfEdgesMesh2D()
    hem2_example.load_from_file('examples/mesh2d.txt')
    print("(A) HalfEdge Structure for 2D OP4-5 :: all half edges")
    for he in hem2_example.half_edges:
        print("(A) HalfEdge Structure for 2D OP4-5 :: vertex and face data of single half edge")
        print(he.vertex.data)
        print(he.face.data)
    print("(A) HalfEdge Structure for 2D OP4-5 :: OP4 - get_triangles_path")
    print(hem2_example.get_triangles_path([(3, 4), (4, 3), (3, 3)], (5, 5)))
    hem2_example.swap_edges([(3, 3), (4, 2), (3, 1)], [(3, 3), (3, 1), (1, 2)])
    print("(A) HalfEdge Structure for 2D OP4-5 :: OP5 - triangles list after edge swap")
    for face in hem2_example.faces:
        print("(A) HalfEdge Structure for 2D OP4-5 :: triangle data (source vertices of each half edge assigned to triangle)")
        print(face.half_edge.vertex.data)
        print(face.half_edge.next_he.vertex.data)
        print(face.half_edge.prev_he.vertex.data)

    # (B) structure with list of vertices and list of connections, op1-3

    bs_example = BasicStructure()
    bs_example.load_from_file(file_mesh)
    print("(B) Basic Structure :: vertices list")
    print(bs_example.vertices)
    print("(B) Basic Structure :: triangles list")
    print(bs_example.triangles)
    print("(B) Basic Structure :: OP1 - get_triangles_by_vertex")
    print(bs_example.get_triangles_by_vertex((0.0, 30.0, 0.0)))
    print("(B) Basic Structure :: OP2 - get_vertex_neighbourhood")
    print(bs_example.get_vertex_neighbourhood((0.0, 30.0, 0.0), 2))
    print("(B) Basic Structure :: OP3 - get_triangle_neighbourhood")
    print(bs_example.get_triangle_neighbourhood([(0.0, 30.0, 0.0), (0.0, 0.0, 30.0), (0.0, 30.0, 30.0)], 2))

    # (B) structure with list of vertices and list of connections for 2d, op4-5

    bs2_example = BasicStructure2D()
    bs2_example.load_from_file('examples/mesh2d.txt')
    print("(B) Basic Structure for 2D OP4-5 :: vertices list")
    print(bs2_example.vertices)
    print("(B) Basic Structure for 2D OP4-5 :: triangles list")
    print(bs2_example.triangles)
    print("(B) Basic Structure for 2D OP4-5 :: OP4 - get_triangles_path")
    print(bs2_example.get_triangles_path([(3, 3), (3, 1), (1, 2)], (5, 5)))
    bs2_example.swap_edges([(3, 3), (4, 2), (3, 1)], [(3, 3), (3, 1), (1, 2)])
    print("(B) Basic Structure for 2D OP4-5 :: OP5 - triangles list after edge swap")
    print(bs2_example.triangles)


hem, hem2d, bs, bs2d = HalfEdgesMesh(), HalfEdgesMesh2D(), BasicStructure(), BasicStructure2D()


def load_stl():
    print("Enter file path (STL format) >> ", end="")
    file_name = input()
    given_mesh = mesh.Mesh.from_file(file_name)

    start_hem = time()
    hem.load_from_file(given_mesh)
    end_hem = time()

    start_bs = time()
    bs.load_from_file(given_mesh)
    end_bs = time()

    print(f"!! Successfully loaded {file_name} as 3D STL mesh file !!")
    print(f"!! Time for HalfEdge: {end_hem-start_hem} !!")
    print(f"!! Time for Basic Structure: {end_bs-start_bs} !!")
    print(f"Vertex example = {hem.vertices[0].data}")
    print(f"Triangle example = {hem.faces[0].data}")


def load_txt():
    print("Enter file path (TXT format) >> ", end="")
    file_name = input()

    start_hem = time()
    hem2d.load_from_file(file_name)
    end_hem = time()

    start_bs = time()
    bs2d.load_from_file(file_name)
    end_bs = time()

    print(f"!! Successfully loaded {file_name} as 2D TXT mesh file !!")
    print(f"!! Time for HalfEdge: {end_hem - start_hem} !!")
    print(f"!! Time for Basic Structure: {end_bs - start_bs} !!")
    print(f"Vertex example = {hem2d.vertices[0].data}")
    print(f"Triangle example = {hem2d.faces[0].data}")


def half_edge():
    while True:
        print("\n===================================================")
        print("[HES] Type the number next to command you want to execute")
        print("[HES] 1. Get triangles by vertex (OP-1)")
        print("[HES] 2. Get vertex neighbourhood (OP-2)")
        print("[HES] 3. Get triangle neighbourhood (OP-3)")
        print("[HES] 4. Get triangles path to vertex (2D, OP-4)")
        print("[HES] 5. Swap edges (2D, OP-5)")
        print("[HES] 6. Exit")
        print("\n[HES] Number >> ", end="")
        he_input = input()

        if he_input == '1':
            if not hem.vertices:
                load_stl()

            print("Enter vertex data as \'x y z\' >> ", end="")
            data = input().split()
            if len(data) == 3:
                coord = tuple([float(c) for c in data])

                start = time()
                triangles_found = hem.get_triangles_by_vertex(coord)
                end = time()

                print(f"!! Time : {end - start}!!")

                print("Triangles found:")
                for t in triangles_found:
                    print(t)
            else:
                print(f"Expected 3, got {len(data)} arguments, !")

        elif he_input == '2':
            if not hem.vertices:
                load_stl()

            print("Enter vertex data and number of layers as \'x y z n\'  >> ", end="")
            data = input().split()
            if len(data) == 4:
                coord = tuple([float(c) for c in data[:3]])

                start = time()
                vertices_found = hem.get_vertex_neighbourhood(coord, int(data[3]))
                end = time()

                print(f"!! Time : {end - start}!!")

                print("Vertices found:")
                for v in vertices_found:
                    print(v)
            else:
                print(f"Expected 4, got {len(data)} arguments!")

        elif he_input == '3':
            if not hem.vertices:
                load_stl()

            print("Enter triangle data and number of layers as \'x1 y1 z1 x2 y2 z2 x3 y3 z3 n\'  >> ", end="")
            data = input().split()
            if len(data) == 10:
                coord = [tuple([float(c) for c in data[i:i+3]]) for i in range(0, 9, 3)]

                start = time()
                triangles_found = hem.get_triangle_neighbourhood(coord, int(data[9]))
                end = time()

                print(f"!! Time : {end - start}!!")

                print("Triangles found:")
                for t in triangles_found:
                    print(t)
            else:
                print(f"Expected 10, got {len(data)} arguments!")

        elif he_input == '4':
            if not hem2d.vertices:
                load_txt()

            print("Enter triangle data and vertex data as \'x1 y1 x2 y2 x3 y3 a b \'  >> ", end="")
            data = input().split()
            if len(data) == 8:
                t_coord = [tuple([float(c) for c in data[i:i+2]]) for i in range(0, 6, 2)]
                v_coord = tuple([float(c) for c in data[6:8]])

                start = time()
                triangles_path = hem2d.get_triangles_path(t_coord, v_coord)
                end = time()

                print(f"!! Time : {end - start}!!")

                print("Triangles found:")
                for t in triangles_path:
                    print(t)
            else:
                print(f"Expected 8, got {len(data)} arguments!")

        elif he_input == '5':
            if not hem2d.vertices:
                load_txt()

            print("Enter triangles data as \'x1 y1 x2 y2 x3 y3 a1 b1 a2 b2 a3 b3 \'  >> ", end="")
            data = input().split()
            if len(data) == 12:
                t_coord1 = [tuple([float(c) for c in data[i:i + 2]]) for i in range(0, 6, 2)]
                t_coord2 = [tuple([float(c) for c in data[i:i + 2]]) for i in range(6, 12, 2)]

                start = time()
                hem2d.swap_edges(t_coord1, t_coord2)
                end = time()

                print(f"!! Time : {end - start}!!")
            else:
                print(f"Expected 12, got {len(data)} arguments!")

        elif he_input == '6':
            print("[HES] Exit...")
            break


def basic():
    while True:
        print("\n===================================================")
        print("[BS] Type the number next to command you want to execute")
        print("[BS] 1. Get triangles by vertex (OP-1)")
        print("[BS] 2. Get vertex neighbourhood (OP-2)")
        print("[BS] 3. Get triangle neighbourhood (OP-3)")
        print("[BS] 4. Get triangles path to vertex (2D, OP-4)")
        print("[BS] 5. Swap edges (2D, OP-5)")
        print("[BS] 6. Exit")
        print("\n[BS] Number >> ", end="")
        bs_input = input()

        if bs_input == '1':
            if not bs.vertices:
                load_stl()

            print("Enter vertex data as \'x y z\' >> ", end="")
            data = input().split()
            if len(data) == 3:
                coord = tuple([float(c) for c in data])

                start = time()
                triangles_found = bs.get_triangles_by_vertex(coord)
                end = time()

                print(f"!! Time : {end - start}!!")

                print("Triangles found:")
                for t in triangles_found:
                    print(t)
            else:
                print(f"Expected 3, got {len(data)} arguments!")

        elif bs_input == '2':
            if not bs.vertices:
                load_stl()

            print("Enter vertex data and number of layers as \'x y z n\'  >> ", end="")
            data = input().split()
            if len(data) == 4:
                coord = tuple([float(c) for c in data[:3]])

                start = time()
                vertices_found = bs.get_vertex_neighbourhood(coord, int(data[3]))
                end = time()

                print(f"!! Time : {end - start}!!")

                print("Vertices found:")
                for v in vertices_found:
                    print(v)
            else:
                print(f"Expected 4, got {len(data)} arguments!")

        elif bs_input == '3':
            if not bs.vertices:
                load_stl()

            print("Enter triangle data and number of layers as \'x1 y1 z1 x2 y2 z2 x3 y3 z3 n\'  >> ", end="")
            data = input().split()
            if len(data) == 10:
                coord = [tuple([float(c) for c in data[i:i + 3]]) for i in range(0, 9, 3)]

                start = time()
                triangles_found = bs.get_triangle_neighbourhood(coord, int(data[9]))
                end = time()

                print(f"!! Time : {end - start}!!")

                print("Triangles found:")
                for t in triangles_found:
                    print(t)
            else:
                print(f"Expected 10, got {len(data)} arguments!")

        elif bs_input == '4':
            if not bs2d.vertices:
                load_txt()

            print("Enter triangle data and vertex data as \'x1 y1 x2 y2 x3 y3 a b \'  >> ", end="")
            data = input().split()
            if len(data) == 8:
                t_coord = [tuple([float(c) for c in data[i:i + 2]]) for i in range(0, 6, 2)]
                v_coord = tuple([float(c) for c in data[6:8]])

                start = time()
                triangles_path = bs2d.get_triangles_path(t_coord, v_coord)
                end = time()

                print(f"!! Time : {end - start}!!")

                print("Triangles found:")
                for t in triangles_path:
                    print(t)
            else:
                print(f"Expected 8, got {len(data)} arguments!")

        elif bs_input == '5':
            if not bs2d.vertices:
                load_txt()

            print("Enter triangles data as \'x1 y1 x2 y2 x3 y3 a1 b1 a2 b2 a3 b3 \'  >> ", end="")
            data = input().split()
            if len(data) == 12:
                t_coord1 = [tuple([float(c) for c in data[i:i + 2]]) for i in range(0, 6, 2)]
                t_coord2 = [tuple([float(c) for c in data[i:i + 2]]) for i in range(6, 12, 2)]

                start = time()
                bs2d.swap_edges(t_coord1, t_coord2)
                end = time()

                print(f"!! Time : {end - start}!!")
            else:
                print(f"Expected 8, got {len(data)} arguments!")

        elif bs_input == '6':
            print("[BS] Exit...")
            break


def plot_3d():
    print("Enter STL file name >> ", end="")
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    imported_mesh = mesh.Mesh.from_file(input())
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(imported_mesh.vectors, edgecolor=['black']))
    scale = imported_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    pyplot.show()


def run():
    print("===================================================")
    print("===== Welcome to the STL File Format loader! ======")
    while True:
        print("\n===================================================")
        print("Type the number next to command you want to execute")
        print("1. Load 3D mesh (STL)")
        print("2. Load 2D mesh (TXT)")
        print("3. HalfEdge Structure")
        print("4. Basic Structure")
        print("5. Plot 3D mesh (STL)")
        print("6. Exit")
        print("\nNumber >> ", end="")
        main_input = input()
        if main_input == '1':
            load_stl()
        elif main_input == '2':
            load_txt()
        elif main_input == '3':
            half_edge()
        elif main_input == '4':
            basic()
        elif main_input == '5':
            plot_3d()
        elif main_input == '6':
            print("Exit...")
            break


def main_function():
    # example_test()
    run()


if __name__ == '__main__':
    main_function()
