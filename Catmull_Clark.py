import openmesh as om

def mid_point(point_a, point_b):
    return [(a+b)/2 for a,b in zip(point_a, point_b)]

def to_tuple(coordinate):
    return (coordinate[0], coordinate[1], coordinate[2])

def preprocess(mesh):
    #第一步，把原网格化为纯四边形网格
    new_faces = []
    for face in mesh.faces():
        vertexes = mesh.fv(face)
        n = len(list(vertexes))
        if n == 4:
            f = []
            v = list(vertexes)
            for i in range(n):
                f.append(mesh.point(v[i]))
            new_faces.append(f)
        else:
            new_points = []
            x = 0
            y = 0
            z = 0
            for vertex in vertexes:
                v = mesh.point(vertex)
                x += v[0] / n
                y += v[1] / n
                z += v[2] / n
            face_point = [x, y, z]
            for halfedge in mesh.fh(face):
                fvertex = mesh.point(mesh.from_vertex_handle(halfedge))
                tvertex = mesh.point(mesh.to_vertex_handle(halfedge))
                new_points.append(fvertex)
                new_points.append(mid_point(fvertex, tvertex))
            for i in range(n):
                new_faces.append([face_point, new_points[2*i-1], new_points[2*i], new_points[2*i+1]])
    #得到纯四边形网格的面的数据
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
        if to_tuple(f[3]) not in new_vertexes:
            v3 = new_mesh.add_vertex(f[3])
            new_vertexes[to_tuple(f[3])] = v3
        else:
            v3 = new_vertexes[to_tuple(f[3])]
        new_mesh.add_face(v0, v1, v2, v3)
    return new_mesh

def new_point_from_halfedge(mesh, halfedge):
    fvertex = mesh.point(mesh.from_vertex_handle(halfedge))
    tvertex = mesh.point(mesh.to_vertex_handle(halfedge))
    ec = mid_point(fvertex, tvertex)
    opposite = mesh.opposite_halfedge_handle(halfedge)
    fp1 = new_point_from_face(mesh, mesh.face_handle(halfedge))
    fp2 = new_point_from_face(mesh, mesh.face_handle(opposite))
    fpc = mid_point(fp1, fp2)
    return mid_point(ec, fpc)

def new_point_from_face(mesh, face):
    vertexes = mesh.fv(face)
    x = 0 
    y = 0
    z = 0
    for vertex in vertexes:
        v = mesh.point(vertex)
        x += v[0] / 4
        y += v[1] / 4
        z += v[2] / 4
    return [x, y, z]

def new_position_of_old_point(mesh, old_point):
    face_points = []
    edge_points = []
    #遍历old_point的所有邻面
    for f in mesh.vf(old_point):
        face_points.append(new_point_from_face(mesh, f))
    #遍历old_point的所有出边
    for h in mesh.voh(old_point):
        edge_points.append(new_point_from_halfedge(mesh, h))
    N = len(face_points)
    v = mesh.point(old_point)
    x = v[0] * (N - 3) / N 
    y = v[1] * (N - 3) / N 
    z = v[2] * (N - 3) / N 
    for v in face_points:
        x += v[0] / (N * N)
        y += v[1] / (N * N)
        z += v[2] / (N * N)
    for v in edge_points:
        x += v[0] * 2 / (N * N)
        y += v[1] * 2 / (N * N)
        z += v[2] * 2 / (N * N)
    return [x, y, z]

def new_faces_from_face(mesh,face):
    list_halfedge = list(mesh.fh(face))
    new_points = []
    for h in list_halfedge:
        new_points.append(new_position_of_old_point(mesh, mesh.from_vertex_handle(h)))
        new_points.append(new_point_from_halfedge(mesh, h))
    face_point = new_point_from_face(mesh, face)
    new_faces = []
    for i in range(4):
        new_faces.append([face_point, new_points[2*i-1], new_points[2*i], new_points[2*i+1]])
    return new_faces

def mesh_subdivision(mesh):        
    mesh = preprocess(mesh)
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
        if to_tuple(f[3]) not in new_vertexes:
            v3 = new_mesh.add_vertex(f[3])
            new_vertexes[to_tuple(f[3])] = v3
        else:
            v3 = new_vertexes[to_tuple(f[3])]
        new_mesh.add_face(v0, v1, v2, v3)
    return new_mesh
