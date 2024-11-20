# renderer.py

import numpy as np
import os

class Renderer:
    def __init__(self, screen_width=80, screen_height=40):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def project(self, vertex, view_matrix):
        homogeneous_vertex = np.array([vertex.x, vertex.y, vertex.z, 1])
        projected_vertex = np.dot(view_matrix, homogeneous_vertex)

        if projected_vertex[3] != 0:
            x_2d = projected_vertex[0] / projected_vertex[3]
            y_2d = projected_vertex[1] / projected_vertex[3]
            return (x_2d, y_2d)
        return None

    def calculate_lighting(self, normal, light_direction):
        intensity = max(np.dot(normal, light_direction), 0)
        return intensity

    def get_ansi_color(self, color):
        return f"\033[38;2;{color.r};{color.g};{color.b}m"

    def render(self, objects, camera):
        view_matrix = camera.get_view_matrix()
        screen_buffer = [[' ' for _ in range(self.screen_width)] for _ in range(self.screen_height)]

        for obj in objects:
            color_code = self.get_ansi_color(obj.color)
            for vertex in obj.vertices:
                projected_vertex = self.project(vertex, view_matrix)
                if projected_vertex:
                    x, y = int(projected_vertex[0] * (self.screen_width // 4)), int(projected_vertex[1] * (self.screen_height // 4))
                    if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                        screen_buffer[y][x] = color_code + '#' + "\033[0m"  # Отображаем точку с цветом

        os.system('cls' if os.name == 'nt' else 'clear')

        for row in screen_buffer:
            print(''.join(row))