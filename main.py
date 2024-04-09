import pygame
import datetime
import numpy as np

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

d = 500

cuboid_colors = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
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

cuboids_edges = [
    edges[0:12],
    edges[12:24],
    edges[24:36],
    edges[36:48]
]


def project(vertex):
    x, y, z = vertex
    near = 0.1
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

def draw():
    screen.fill(BLACK)
    for cuboid_index, cuboid_edges in enumerate(cuboids_edges):
        color = cuboid_colors[cuboid_index % len(cuboid_colors)]
        for edge in cuboid_edges:
            points = []
            for vertex_index in edge:
                vertex = vertices[vertex_index]
                point = project(vertex)
                if point is not None:
                    points.append(point)

            if len(points) == 2:
                pygame.draw.line(screen, color, points[0], points[1], 1)
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
                vertices = rotate_x(vertices, 5)
            elif event.key == pygame.K_y:
                vertices = rotate_y(vertices, 5)
            elif event.key == pygame.K_z:
                vertices = rotate_z(vertices, 5)
            elif event.key == pygame.K_n:
                d *= 0.9
            elif event.key == pygame.K_m:
                d *= 1.1
            elif event.key == pygame.K_s:
                filename = f"screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
                pygame.image.save(screen, filename)
    draw()

pygame.quit()
