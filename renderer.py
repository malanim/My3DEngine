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

        if abs(projected_vertex[3]) > 1e-6:
            w = projected_vertex[3]
            if camera.projection_type == "perspective":
                x_2d = projected_vertex[0] / w
                y_2d = projected_vertex[1] / w
            else:  # orthographic
                # Масштабируем координаты для ортографической проекции
                scale = 0.5  # Коэффициент масштабирования
                x_2d = projected_vertex[0] * scale
                y_2d = projected_vertex[1] * scale
            
            # Общая проверка границ видимости
            if -1 <= x_2d <= 1 and -1 <= y_2d <= 1:
                return (x_2d, y_2d)
        return None

    def calculate_lighting(self, point, normal, light, camera_pos):
        """Вычисляет интенсивность освещения с учетом позиции точки и затухания света."""
        # Вектор направления к источнику света
        to_light = light.position - point
        distance = to_light.length()
        light_dir = to_light.normalize()

        # Вектор направления к камере для расчета бликов
        view_dir = (Vector3(*camera_pos) - point).normalize()
        
        # Ambient компонент (фоновое освещение)
        ambient = 0.2
        
        # Диффузное освещение с улучшенным коэффициентом
        diffuse = max(0.1, normal.dot(light_dir))
        
        # Улучшенное затухание света с расстоянием
        attenuation = min(1.0, 1.0 / (1.0 + distance * 0.1))
        
        # Улучшенное отражение света (блики)
        reflect_dir = (light_dir - normal * (2.0 * normal.dot(light_dir))).normalize()
        specular = pow(max(0, view_dir.dot(reflect_dir)), 16)  # Уменьшили степень для более мягких бликов
        
        # Комбинируем все компоненты освещения с улучшенными весами
        return (ambient + diffuse * 0.6 + specular * 0.2) * attenuation * light.intensity

    def get_ansi_color(self, color):
        return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

    def get_symbol_from_intensity(self, intensity):
        """Возвращает символ на основе интенсивности освещения."""
        # Расширенная градация символов для более плавного перехода
        symbols = ' ·.,:;+*#▒▓█'
        index = min(int(intensity * len(symbols)), len(symbols) - 1)
        return symbols[index]

    def render(self, objects, camera, lights):
        # Save original light positions
        original_positions = [light.copy_position() for light in lights]
        
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

                # Вычисляем освещение для каждой вершины грани
                vertex_intensities = []
                for vertex_index in face:
                    vertex = obj.vertices[vertex_index]
                    intensity = self.calculate_lighting(
                        vertex,
                        normal,
                        lights[0],
                        camera.position
                    )
                    vertex_intensities.append(intensity)
                
                # Интерполируем освещение для каждой точки грани
                for y in range(min_y, max_y + 1):
                    for x in range(min_x, max_x + 1):
                        if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                            # Вычисляем барицентрические координаты для интерполяции
                            total_area = 0
                            weights = []
                            point = Vector3(x, y, 0)
                            
                            for i in range(len(projected_vertices)):
                                v1 = Vector3(projected_vertices[i][0], projected_vertices[i][1], 0)
                                v2 = Vector3(projected_vertices[(i+1)%len(projected_vertices)][0], 
                                           projected_vertices[(i+1)%len(projected_vertices)][1], 0)
                                area = abs((v2 - v1).cross(point - v1).z)
                                total_area += area
                                weights.append(area)
                            
                            if total_area > 0:
                                # Нормализуем веса
                                weights = [w/total_area for w in weights]
                                
                                # Интерполируем интенсивность
                                interpolated_intensity = sum(w * i for w, i in zip(weights, vertex_intensities))
                                
                                # Применяем глубину и символ
                                current_depth = sum(obj.vertices[vi].z for vi in face) / len(face)
                                if current_depth < depth_buffer[y][x]:
                                    depth_buffer[y][x] = current_depth
                                    symbol = self.get_symbol_from_intensity(interpolated_intensity)
                                    screen_buffer[y][x] = color_code + symbol

        # Restore original light positions
        for light, orig_pos in zip(lights, original_positions):
            light.position = orig_pos
            
        # Выводим экранный буфер
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in screen_buffer:
            print(''.join(row) + "\033[0m")  # Сбрасываем цвет после каждой строки