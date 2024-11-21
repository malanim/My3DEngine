# camera.py

import numpy as np
from vector import Vector3

class Camera:
    def __init__(self, position, direction, up_vector, projection_type="perspective", fov=45, near=0.1, far=100):
        self.position = position.to_numpy()
        self.direction = direction.normalize()
        self.up_vector = up_vector.normalize()
        self.projection_type = projection_type
        self.fov = fov
        self.near = near
        self.far = far
        self.aspect_ratio = 2.0  # Учитываем, что символы в консоли прямоугольные
        
        # Настраиваем позицию камеры для вида сверху-сбоку
        if self.projection_type == "orthographic":
            self.position[2] *= 2.5
        else:
            # Поднимаем камеру выше и отодвигаем дальше
            self.position[1] *= 1.5  # Поднимаем выше
            self.position[2] *= 2.0  # Отодвигаем дальше
        
        # Проверка на нулевые векторы
        if self.direction.length() == 0 or self.up_vector.length() == 0:
            raise ValueError("Direction and up_vector cannot be zero vectors.")
        
        # Обновление оси X и Y
        self.update_axes()

    def update(self, position, direction):
        self.position = position.to_numpy()  # Преобразуем вектор в массив NumPy
        self.direction = direction.normalize()
        
        if self.direction.length() == 0:
            raise ValueError("Direction cannot be a zero vector.")
        
        self.update_axes()

    def update_axes(self):
        z_axis = self.direction.to_numpy()  # Направление взгляда как массив NumPy

        # Проверка на нулевые векторы перед вычислением векторного произведения
        if np.linalg.norm(self.up_vector.to_numpy()) == 0 or np.linalg.norm(z_axis) == 0:
            raise ValueError("Up vector or direction cannot be zero vectors.")

        x_axis = np.cross(self.up_vector.to_numpy(), z_axis)  # Вправо
        if np.linalg.norm(x_axis) == 0:
            raise ValueError("Up vector and direction are collinear; cannot define a right axis.")
        
        x_axis = x_axis / np.linalg.norm(x_axis)  # Нормализация оси X
        y_axis = np.cross(z_axis, x_axis)  # Вверх
        y_axis = y_axis / np.linalg.norm(y_axis)  # Нормализация оси Y

        self.view_matrix = np.array([
            [x_axis[0], y_axis[0], z_axis[0], 0],
            [x_axis[1], y_axis[1], z_axis[1], 0],
            [x_axis[2], y_axis[2], z_axis[2], 0],
            [-np.dot(x_axis, self.position), -np.dot(y_axis, self.position), -np.dot(z_axis, self.position), 1]
        ])

    def get_projection_matrix(self):
        if self.projection_type == "perspective":
            # Улучшенная матрица перспективной проекции
            f = 1.0 / np.tan(np.radians(self.fov) / 2.0)
            z_range = self.far - self.near
            a = self.aspect_ratio
            
            # Улучшенная матрица перспективной проекции с учетом aspect ratio
            return np.array([
                [f/a, 0, 0, 0],
                [0, f, 0, 0],
                [0, 0, -(self.far + self.near)/z_range, -(2*self.far*self.near)/z_range],
                [0, 0, -1, 0]
            ]) * 0.5  # Уменьшаем масштаб для лучшей видимости
        else:  # orthographic
            # Создаем матрицу ортографической проекции
            scale = 1.0
            return np.array([
                [scale/self.aspect_ratio, 0, 0, 0],
                [0, scale, 0, 0],
                [0, 0, -2/(self.far-self.near), -(self.far+self.near)/(self.far-self.near)],
                [0, 0, 0, 1]
            ])

    def get_view_matrix(self):
        return self.view_matrix

    def get_full_matrix(self):
        return np.dot(self.get_projection_matrix(), self.view_matrix)