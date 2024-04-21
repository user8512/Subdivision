import openmesh as om
import math

def to_tuple(coordinate):
    return (coordinate[0], coordinate[1], coordinate[2])

def new_point_from_face(mesh,face):
    vertexes = mesh.fv(face)
    x = 0
    y = 0
    z = 0
    for vertex in vertexes:
        v = mesh.point(vertex)
        x += v[0] / 3
        y += v[1] / 3
        z += v[2] / 3
    return [x, y, z]

def new_position_of_old_point(mesh,old_point):
    neighbors = mesh.vv(old_point)
    n = len(list(neighbors))
    an = (4 - math.cos(2 * math.pi / n)) / 9
    v = mesh.point(old_point)
    x = (1 - an) * v[0]
    y = (1 - an) * v[1]
    z = (1 - an) * v[2]
    u = an / n
    for neighbor in neighbors:
        v = mesh.point(neighbor)
        x += u * v[0]
        y += u * v[1]
        z += u * v[2]
    return [x, y, z]

def new_faces_from_point(mesh, point):
    new_faces = []
    face_points = []
    for face in mesh.vf(point):
        face_points.append(new_point_from_face(mesh, face))
    new_point = new_position_of_old_point(mesh, point)
    for i in range(len(face_points)):
        new_faces.append([new_point, face_points[i], face_points[i-1]])
    return new_faces

def mesh_subdivision(mesh):   
    new_faces = []
    for v in mesh.vertices():
        new_faces = new_faces + new_faces_from_point(mesh,v)
    new_mesh = om.PolyMesh()
    new_vertexes = {}
    for f in new_faces:
        #add_vertex产生新的vertex handle，而每个顶点对应的handle必须唯一，故用字典记录保证唯一性
        if to_tuple(f[0]) not in new_vertexes:
            v0 = new_mesh.add_vertex(f[0])
            new_vertexes[to_tuple(f[0])] = v0
        else:
            v0 = new_vertexes[to_tuple(f[0])]
        if to_tuple(f[1]) not in new_vertexes:
            v1 = new_mesh.add_vertex(f[1])
            new_vertexes[to_tuple(f[1])] = v1
        else:
            v1 = new_vertexes[to_tuple(f[1])]
        if to_tuple(f[2]) not in new_vertexes:
            v2 = new_mesh.add_vertex(f[2])
            new_vertexes[to_tuple(f[2])] = v2
        else:
            v2 = new_vertexes[to_tuple(f[2])]
        new_mesh.add_face(v0, v1, v2)
    return new_mesh