# object.py

import math
from vector import Vector3  # Импортируем класс Vector3 из файла vector.py

DEBUG = False  # Установите True для включения отладки

class Object3D:
    def __init__(self, vertices, faces, color):
        self.vertices = vertices  # Список вершин (объекты Vector3)
        self.faces = faces        # Список граней (индексы вершин)
        self.color = color        # Цвет объекта

    def transform(self, matrix):
        """Применяет матрицу трансформации к вершинам объекта."""
        self.vertices = [matrix * v for v in self.vertices]  # Умножаем матрицу на каждую вершину

    def calculate_normals(self):
        """Вычисляет нормали для каждой грани объекта."""
        normals = [None] * len(self.faces)  # Инициализация списка нормалей с None
        if DEBUG:
            print(f"Количество вершин: {len(self.vertices)}")
            print(f"Количество граней: {len(self.faces)}")

        for i, face in enumerate(self.faces):
            if DEBUG:
                print(f"Обрабатываем грань: {face}")
            if len(face) < 3:  # Убедитесь, что грань состоит как минимум из 3 вершин
                continue
            
            # Проверяем индексы перед доступом
            for index in face:
                if index >= len(self.vertices):
                    if DEBUG:
                        print(f"Ошибка: индекс {index} выходит за пределы вершин.")
                    return normals  # Завершаем выполнение, если индекс неверный

            # Получаем вершины грани
            v1 = self.vertices[face[1]] - self.vertices[face[0]]
            v2 = self.vertices[face[2]] - self.vertices[face[0]]

            # Выводим векторы для отладки
            if DEBUG:
                print(f"v1: {v1}, v2: {v2}")

            # Проверяем, не нулевые ли векторы
            if v1.length() == 0 or v2.length() == 0:
                if DEBUG:
                    print("Ошибка: один из векторов равен нулю.")
                continue
            
            # Вычисляем нормаль с помощью векторного произведения
            normal = v1.cross(v2)
            
            # Проверяем, не является ли нормаль нулевым вектором
            if normal.length() == 0:
                if DEBUG:
                    print("Ошибка: нормаль равна нулю, пропускаем.")
                continue
            
            normal = normal.normalize()
            normals[i] = normal  # Сохраняем нормаль в соответствующий индекс
        return normals

class Cube(Object3D):
    def __init__(self, size=1, color=(255, 255, 255)):
        half_size = size / 2
        vertices = [
            Vector3(-half_size, -half_size, -half_size),
            Vector3(half_size, -half_size, -half_size),
            Vector3(half_size, half_size, -half_size),
            Vector3(-half_size, half_size, -half_size),
            Vector3(-half_size, -half_size, half_size),
            Vector3(half_size, -half_size, half_size),
            Vector3(half_size, half_size, half_size),
            Vector3(-half_size, half_size, half_size),
        ]
        faces = [
            (0, 1, 2, 3),  # Передняя грань
            (4, 5, 6, 7),  # Задняя грань
            (0, 1, 5, 4),  # Нижняя грань
            (2, 3, 7, 6),  # Верхняя грань
            (0, 3, 7, 4),  # Левая грань
            (1, 2, 6, 5),  # Правая грань
        ]
        super().__init__(vertices, faces, color)

class Plane(Object3D):
    def __init__(self, width=1, height=1, color=(255, 255, 255)):
        half_width = width / 2
        half_height = height / 2
        vertices = [
            Vector3(-half_width, -half_height, 0),  # Нижний левый угол
            Vector3(half_width, -half_height, 0),   # Нижний правый угол
            Vector3(half_width, half_height, 0),    # Верхний правый угол
            Vector3(-half_width, half_height, 0),   # Верхний левый угол
        ]
        faces = [
            (0, 1, 2, 3),  # Единая грань плоскости
        ]
        super().__init__(vertices, faces, color)

class Sphere(Object3D):
    def __init__(self, radius=1, color=(255, 255, 255), segments=12):
        self.vertices = []
        self.faces = []
        self.color = color

        # Генерация вершин
        for i in range(segments + 1):
            theta = i * math.pi / segments  # Угол по вертикали
            for j in range(segments + 1):
                phi = j * 2 * math.pi / segments  # Угол по горизонтали
                x = radius * math.sin(theta) * math.cos(phi)
                y = radius * math.sin(theta) * math.sin(phi)
                z = radius * math.cos(theta)
                self.vertices.append(Vector3(x, y, z))

        # Генерация граней
        for i in range(segments):
            for j in range(segments):
                first = (i * (segments + 1)) + j
                second = first + segments + 1
                # Проверяем, чтобы индексы не выходили за пределы
                if second + 1 < len(self.vertices) and first + 1 < len(self.vertices):
                    self.faces.append((first, second, second + 1, first + 1))

        super().__init__(self.vertices, self.faces, color)

        # Проверьте количество вершин и граней
        # print(f"Количество вершин: {len(self.vertices)}")
        # print(f"Количество граней: {len(self.faces)}")
class Cylinder(Object3D):
    def __init__(self, radius=1, height=2, color=(255, 255, 255), segments=12):
        self.vertices = []
        self.faces = []
        self.color = color

        # Генерация вершин
        for i in range(segments):
            angle = i * 2 * math.pi / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.vertices.append(Vector3(x, y, -height / 2))  # Нижняя грань
            self.vertices.append(Vector3(x, y, height / 2))   # Верхняя грань

        # Генерация граней
        for i in range(segments):
            next_index = (i + 1) % segments
            self.faces.append((i * 2, next_index * 2, next_index * 2 + 1, i * 2 + 1))

        super().__init__(self.vertices, self.faces, color)