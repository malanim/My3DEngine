# renderer.py

import numpy as np
import os
from vector import Vector3

DEBUG = False  # Установите True для включения отладки

class Renderer:
    def __init__(self, screen_width=80, screen_height=40):
        # Terminal characters are typically about twice as tall as they are wide
        # So we adjust the width to compensate for this
        self.screen_width = screen_width * 2  # Double the width to compensate for character aspect ratio
        self.screen_height = screen_height

    def project(self, vertex, camera):
        homogeneous_vertex = np.array([vertex.x, vertex.y, vertex.z, 1])
        full_matrix = camera.get_full_matrix()
        projected_vertex = np.dot(full_matrix, homogeneous_vertex)

        if projected_vertex[3] != 0:
            w = projected_vertex[3]
            if camera.projection_type == "perspective":
                x_2d = projected_vertex[0] / w
                y_2d = projected_vertex[1] / w
            else:  # orthographic
                x_2d = projected_vertex[0]
                y_2d = projected_vertex[1]
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
        # Создаем буфер глубины для правильного отображения перекрывающихся граней
        screen_buffer = [[' ' for _ in range(self.screen_width)] for _ in range(self.screen_height)]
        depth_buffer = [[float('inf') for _ in range(self.screen_width)] for _ in range(self.screen_height)]

        for obj in objects:
            normals = obj.calculate_normals()
            color_code = self.get_ansi_color(obj.color)
            
            # Сортируем грани по Z-координате (для правильного порядка отрисовки)
            faces_with_depth = []
            for i, face in enumerate(obj.faces):
                if i >= len(normals) or normals[i] is None:
                    continue
                # Вычисляем среднюю Z-координату грани
                z_avg = sum(obj.vertices[vi].z for vi in face) / len(face)
                faces_with_depth.append((face, normals[i], z_avg))
            
            # Сортируем грани от дальних к ближним
            faces_with_depth.sort(key=lambda x: x[2], reverse=True)
            
            for face, normal, _ in faces_with_depth:
                # Проецируем все вершины грани
                projected_vertices = []
                for vertex_index in face:
                    vertex = obj.vertices[vertex_index]
                    projected = self.project(vertex, camera)
                    if projected:
                        x = int((projected[0] + 1) * self.screen_width // 2)
                        y = int((projected[1] + 1) * self.screen_height // 2)
                        if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                            projected_vertices.append((x, y))

                if len(projected_vertices) < 3:
                    continue

                # Находим границы грани
                min_x = max(0, min(v[0] for v in projected_vertices))
                max_x = min(self.screen_width - 1, max(v[0] for v in projected_vertices))
                min_y = max(0, min(v[1] for v in projected_vertices))
                max_y = min(self.screen_height - 1, max(v[1] for v in projected_vertices))

                # Центр грани для расчета освещения
                center_vertex = sum((obj.vertices[vi] for vi in face), Vector3(0,0,0))
                center_vertex = center_vertex * (1.0 / len(face))
                
                # Рассчитываем освещение для всей грани
                light_direction = (lights[0].position - center_vertex).normalize()
                intensity = self.calculate_lighting(normal, light_direction)
                symbol = self.get_symbol_from_intensity(intensity)

                # Заполняем область грани с учетом глубины
                for y in range(min_y, max_y + 1):
                    for x in range(min_x, max_x + 1):
                        # Проверяем, находится ли точка внутри грани
                        if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                            current_depth = sum(obj.vertices[vi].z for vi in face) / len(face)
                            if current_depth < depth_buffer[y][x]:
                                depth_buffer[y][x] = current_depth
                                screen_buffer[y][x] = color_code + symbol

        # Выводим экранный буфер
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in screen_buffer:
            print(''.join(row) + "\033[0m")  # Сбрасываем цвет после каждой строки