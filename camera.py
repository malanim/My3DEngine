# camera.py

import numpy as np
from vector import Vector3

class Camera:
    def __init__(self, position, direction, up_vector):
        self.position = position.to_numpy()  # Преобразуем вектор в массив NumPy
        self.direction = direction.normalize()  # Нормализация направления
        self.up_vector = up_vector.normalize()  # Нормализация вверх-вектора
        
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

    def get_view_matrix(self):
        return self.view_matrix