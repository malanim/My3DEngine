# renderer.py

import numpy as np
import os

DEBUG = False  # Установите True для включения отладки

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
        """Вычисляет интенсивность освещения на основе нормали и направления света."""
        light_direction = light_direction.normalize()  # Нормализуем направление света
        intensity = max(0, normal.dot(light_direction))  # Вычисляем интенсивность
        return intensity

    def get_ansi_color(self, color):
        return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

    def get_symbol_from_intensity(self, intensity):
        """Возвращает символ на основе интенсивности освещения."""
        if intensity > 0.8:
            return '█'  # Full Block
        elif intensity > 0.6:
            return '▓'  # Dark Shade
        elif intensity > 0.4:
            return '▒'  # Medium Shade
        elif intensity > 0.2:
            return '░'  # Light Shade
        else:
            return ' '  # Space

    def render(self, objects, camera, lights):
        view_matrix = camera.get_view_matrix()
        screen_buffer = [[' ' for _ in range(self.screen_width)] for _ in range(self.screen_height)]

        for obj in objects:
            normals = obj.calculate_normals()  # Получаем нормали для текущего объекта
            color_code = self.get_ansi_color(obj.color)
            
            for i, face in enumerate(obj.faces):
                # Проверяем, существует ли нормаль для текущей грани
                if i >= len(normals) or normals[i] is None:
                    if DEBUG:
                        print(f"Пропускаем грань {i} из-за отсутствия нормали.")
                    continue  # Пропускаем, если нормали нет
                
                normal = normals[i]
                for vertex_index in face:
                    vertex = obj.vertices[vertex_index]
                    projected_vertex = self.project(vertex, view_matrix)
                    if projected_vertex:
                        x, y = int(projected_vertex[0] * (self.screen_width // 4)), int(projected_vertex[1] * (self.screen_height // 4))
                        if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                            # Рассчитайте направление 
                            light_direction = (lights[0].position - vertex).normalize()  # Предполагаем, что у нас есть хотя бы один источник света
                            intensity = self.calculate_lighting(normal, light_direction)
                            symbol = self.get_symbol_from_intensity(intensity)  # Получаем символ на основе интенсивности
                            screen_buffer[y][x] = color_code + symbol  # Используем символ для отображения

        # Выводим экранный буфер
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in screen_buffer:
            print(''.join(row) + "\033[0m")  # Сбрасываем цвет после каждой строки
