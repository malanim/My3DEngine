# renderer.py

import numpy as np
import os

class Renderer:
    def __init__(self, screen_width=80, screen_height=40):
        self.screen_width = screen_width
        self.screen_height = screen_height

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
        # Получаем матрицу вида
        view_matrix = camera.get_view_matrix()
        # Создаем буфер экрана
        screen_buffer = [[' ' for _ in range(self.screen_width)] for _ in range(self.screen_height)]

        for obj in objects:
            for vertex in obj.vertices:
                projected_vertex = self.project(vertex, view_matrix)
                if projected_vertex:
                    x, y = int(projected_vertex[0] * (self.screen_width // 4)), int(projected_vertex[1] * (self.screen_height // 4))
                    if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                        screen_buffer[y][x] = '#'  # Отображаем точку на экране

        # Очистка экрана
        os.system('cls' if os.name == 'nt' else 'clear')

        # Выводим буфер на экран
        for row in screen_buffer:
            print(''.join(row))