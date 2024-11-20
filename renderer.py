# renderer.py

import numpy as np

class Renderer:
    def __init__(self):
        pass  # Здесь можно инициализировать необходимые переменные, если нужно

    def project(self, vertex, view_matrix):
        # Примените матрицу вида к вершине
        homogeneous_vertex = np.array([vertex.x, vertex.y, vertex.z, 1])
        projected_vertex = np.dot(view_matrix, homogeneous_vertex)
        
        # Перейдите от однородных координат к 2D
        if projected_vertex[3] != 0:
            x_2d = projected_vertex[0] / projected_vertex[3]
            y_2d = projected_vertex[1] / projected_vertex[3]
            return (x_2d, y_2d)
        return None

    def calculate_lighting(self, normal, light_direction):
        intensity = max(np.dot(normal, light_direction), 0)
        return intensity

    def render(self, objects, camera):
        view_matrix = camera.get_view_matrix()
        for obj in objects:
            for vertex in obj.vertices:
                projected_vertex = self.project(vertex, view_matrix)
                if projected_vertex:
                    # Здесь можно добавить код для отображения точки в консоли
                    print(f"Vertex projected to 2D: {projected_vertex}")
