import pygame
import datetime
import numpy as np

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

d = 500
near = 0.1

cuboid_colors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 255, 255),  # Blue
    (255, 255, 0),  # Yellow
]

vertices = [
    [100, 100, 100], [150, 100, 100], [150, -50, 100], [100, -50, 100],
    [100, 100, 200], [150, 100, 200], [150, -50, 200], [100, -50, 200],
    [-50, 100, 100], [0, 100, 100], [0, -50, 100], [-50, -50, 100],
    [-50, 100, 200], [0, 100, 200], [0, -50, 200], [-50, -50, 200],
    [100, 100, 300], [150, 100, 300], [150, -50, 300], [100, -50, 300],
    [100, 100, 400], [150, 100, 400], [150, -50, 400], [100, -50, 400],
    [-50, 100, 300], [0, 100, 300], [0, -50, 300], [-50, -50, 300],
    [-50, 100, 400], [0, 100, 400], [0, -50, 400], [-50, -50, 400]
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
    (8, 9), (9, 10), (10, 11), (11, 8),
    (12, 13), (13, 14), (14, 15), (15, 12),
    (8, 12), (9, 13), (10, 14), (11, 15),
    (16, 17), (17, 18), (18, 19), (19, 16),
    (20, 21), (21, 22), (22, 23), (23, 20),
    (16, 20), (17, 21), (18, 22), (19, 23),
    (24, 25), (25, 26), (26, 27), (27, 24),
    (28, 29), (29, 30), (30, 31), (31, 28),
    (24, 28), (25, 29), (26, 30), (27, 31),
]

faces = [
    (0, 1, 2, 3), (4, 5, 6, 7),
    (0, 1, 5, 4), (3, 2, 6, 7),
    (1, 2, 6, 5), (0, 3, 7, 4),
    (8, 9, 10, 11), (12, 13, 14, 15),
    (8, 9, 13, 12), (11, 10, 14, 15),
    (9, 10, 14, 13), (8, 11, 15, 12),
    (16, 17, 18, 19), (20, 21, 22, 23),
    (16, 17, 21, 20), (19, 18, 22, 23),
    (17, 18, 22, 21), (16, 19, 23, 20),
    (24, 25, 26, 27), (28, 29, 30, 31),
    (24, 25, 29, 28), (27, 26, 30, 31),
    (25, 26, 30, 29), (24, 27, 31, 28)
]

cuboids_edges = [
    edges[0:12],
    edges[12:24],
    edges[24:36],
    edges[36:48]
]

viewer = np.array([0, 0, -1000])


def interpolate(v0, v1, t):
    return v0 + t * (v1 - v0)


def clip_edge(v0, v1):
    t = (near - v0[2]) / (v1[2] - v0[2])
    x = interpolate(v0[0], v1[0], t)
    y = interpolate(v0[1], v1[1], t)
    z = near
    return [x, y, z]


def project(vertex):
    x, y, z = vertex
    if z < near:
        return None

    projection_matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1 / d, 0]
    ])

    homogeneous_vertex = np.array([x, y, z, 1])
    projected_homogeneous_vertex = projection_matrix.dot(homogeneous_vertex)

    projected_vertex = projected_homogeneous_vertex / projected_homogeneous_vertex[3]

    projected_x = int((projected_vertex[0] / projected_vertex[2]) * d + screen_width / 2)
    projected_y = int((-projected_vertex[1] / projected_vertex[2]) * d + screen_height / 2)

    return projected_x, projected_y


def translate(vertices, x_direction, y_direction, z_direction):
    translation_matrix = np.array([
        [1, 0, 0, x_direction],
        [0, 1, 0, y_direction],
        [0, 0, 1, z_direction],
        [0, 0, 0, 1]
    ])

    translated_vertices = []
    for vertex in vertices:
        homogenous_vertex = np.array(vertex + [1])
        translated_vertex = translation_matrix.dot(homogenous_vertex)
        translated_vertices.append(translated_vertex[:-1].tolist())
    return translated_vertices


def rotate_x(vertices, angle):
    cos_a, sin_a = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    rotation_matrix = np.array([
        [1, 0, 0, 0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a, 0],
        [0, 0, 0, 1]
    ])
    rotated_vertices = []
    for vertex in vertices:
        homogenous_vertex = np.array(vertex + [1])
        rotated_vertex = rotation_matrix.dot(homogenous_vertex)
        rotated_vertices.append(rotated_vertex[:-1].tolist())
    return rotated_vertices


def rotate_y(vertices, angle):
    cos_a, sin_a = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    rotation_matrix = np.array([
        [cos_a, 0, sin_a, 0],
        [0, 1, 0, 0],
        [-sin_a, 0, cos_a, 0],
        [0, 0, 0, 1]
    ])
    rotated_vertices = []
    for vertex in vertices:
        homogenous_vertex = np.array(vertex + [1])
        rotated_vertex = rotation_matrix.dot(homogenous_vertex)
        rotated_vertices.append(rotated_vertex[:-1].tolist())
    return rotated_vertices


def rotate_z(vertices, angle):
    cos_a, sin_a = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    rotation_matrix = np.array([
        [cos_a, -sin_a, 0, 0],
        [sin_a, cos_a, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    rotated_vertices = []
    for vertex in vertices:
        homogenous_vertex = np.array(vertex + [1])
        rotated_vertex = rotation_matrix.dot(homogenous_vertex)
        rotated_vertices.append(rotated_vertex[:-1].tolist())
    return rotated_vertices


def clip_edge(v0, v1):
    if v0[2] >= near and v1[2] >= near:
        return [v0, v1]
    if v0[2] >= near > v1[2]:
        return [v0, compute_intersection(v0, v1)]
    if v1[2] >= near > v0[2]:
        return [compute_intersection(v1, v0), v1]
    return []


def compute_intersection(v0, v1):
    t = (near - v0[2]) / (v1[2] - v0[2])
    return [
        interpolate(v0[0], v1[0], t),
        interpolate(v0[1], v1[1], t),
        near
    ]


def draw():
    screen.fill(BLACK)
    cuboid_faces_count = 6

    face_distances = [(i, np.mean([np.linalg.norm(vertices[vertex] - viewer) for vertex in face])) for i, face in enumerate(faces)]

    sorted_faces = sorted(face_distances, key=lambda x: x[1], reverse=True)

    for i, _ in sorted_faces:
        face = faces[i]
        color = cuboid_colors[i // cuboid_faces_count]
        projected_points = []
        clipped_vertices = []

        for j in range(len(face)):
            v0_index, v1_index = face[j], face[(j + 1) % len(face)]
            v0, v1 = vertices[v0_index], vertices[v1_index]

            if v0[2] > near:
                clipped_vertices.append(v0)

            if (v0[2] > near > v1[2]) or (v0[2] < near < v1[2]):
                clipped_vertices.append(compute_intersection(v0, v1))

        for vertex in clipped_vertices:
            projected_point = project(vertex)
            if projected_point:
                projected_points.append(projected_point)

        if len(projected_points) >= 3:
            pygame.draw.polygon(screen, color, [projected_points[0], projected_points[1], projected_points[2]])
            if len(projected_points) == 4:
                pygame.draw.polygon(screen, color, [projected_points[0], projected_points[2], projected_points[3]])

    pygame.display.flip()



running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vertices = translate(vertices, 10, 0, 0)
            elif event.key == pygame.K_RIGHT:
                vertices = translate(vertices, -10, 0, 0)
            elif event.key == pygame.K_UP:
                vertices = translate(vertices, 0, -10, 0)
            elif event.key == pygame.K_DOWN:
                vertices = translate(vertices, 0, 10, 0)
            elif event.key == pygame.K_q:
                vertices = translate(vertices, 0, 0, -10)
            elif event.key == pygame.K_e:
                vertices = translate(vertices, 0, 0, 10)
            elif event.key == pygame.K_x:
                vertices = rotate_x(vertices, 10)
            elif event.key == pygame.K_y:
                vertices = rotate_y(vertices, 10)
            elif event.key == pygame.K_z:
                vertices = rotate_z(vertices, 10)
            elif event.key == pygame.K_d:
                vertices = rotate_x(vertices, -10)
            elif event.key == pygame.K_t:
                vertices = rotate_y(vertices, -10)
            elif event.key == pygame.K_a:
                vertices = rotate_z(vertices, -10)
            elif event.key == pygame.K_n:
                d *= 0.9
            elif event.key == pygame.K_m:
                d *= 1.1
            elif event.key == pygame.K_s:
                filename = f"screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
                pygame.image.save(screen, filename)
    draw()

pygame.quit()
