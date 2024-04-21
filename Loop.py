import openmesh as om

def mid_point(point_a, point_b):
    return [(a+b)/2 for a,b in zip(point_a, point_b)]

def mid_point_4(point_a, point_b, point_c, point_d):
    return [(a+b+c+d)/4 for a,b,c,d in zip(point_a, point_b, point_c, point_d)]

def to_tuple(coordinate):
    return (coordinate[0], coordinate[1], coordinate[2])

def new_point_from_halfedge(mesh,halfedge):
    fvertex = mesh.point(mesh.from_vertex_handle(halfedge))
    tvertex = mesh.point(mesh.to_vertex_handle(halfedge))
    mid = mid_point(fvertex, tvertex)
    next_point = mesh.point(mesh.to_vertex_handle(mesh.next_halfedge_handle(halfedge)))
    opposite = mesh.opposite_halfedge_handle(halfedge)
    opposite_next_point = mesh.point(mesh.to_vertex_handle(mesh.next_halfedge_handle(opposite)))
    mid_4 = mid_point_4(fvertex, tvertex, next_point, opposite_next_point)
    return mid_point(mid, mid_4)

def new_position_of_old_point(mesh,old_point):
    neighbors = mesh.vv(old_point)
    n = len(list(neighbors))
    if(n == 3):
        u = 3 / 16
    else:
        u = 3 / (8 * n)
    v = mesh.point(old_point)
    x = (1 - n * u) * v[0]
    y = (1 - n * u) * v[1]
    z = (1 - n * u) * v[2]
    for neighbor in neighbors:
        v = mesh.point(neighbor)
        x += u * v[0]
        y += u * v[1]
        z += u * v[2]
    return [x, y, z]

def new_faces_from_face(mesh,face):
    list_halfedge = list(mesh.fh(face))
    new_faces = []
    halfedge_points = []
    adjusted_old_points = []
    for i in range(3):
        halfedge = list_halfedge[i]
        adjusted_old_points.append(new_position_of_old_point(mesh,mesh.to_vertex_handle(halfedge)))
        halfedge_points.append(new_point_from_halfedge(mesh,halfedge))
    new_faces.append([halfedge_points[0], halfedge_points[1], halfedge_points[2]])
    new_faces.append([halfedge_points[0], adjusted_old_points[0], halfedge_points[1]])
    new_faces.append([halfedge_points[1], adjusted_old_points[1], halfedge_points[2]])
    new_faces.append([halfedge_points[2], adjusted_old_points[2], halfedge_points[0]])
    return new_faces

def mesh_subdivision(mesh):     
    new_faces = []
    for f in mesh.faces():
        new_faces = new_faces + new_faces_from_face(mesh,f)
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