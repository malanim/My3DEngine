# vector.py

import math
import numpy as np

class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Matrix4):  # Умножение на матрицу
            vec = np.array([self.x, self.y, self.z, 1])  # Однородные координаты
            result = np.dot(other.values, vec)  # Умножаем матрицу на вектор
            return Vector3(result[0], result[1], result[2])  # Возвращаем новый вектор
        elif isinstance(other, (int, float)):  # Умножение на скаляр
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError("Unsupported operand type(s) for *: 'Vector3' and '{}'".format(type(other).__name__))

    def to_numpy(self):
        return np.array([self.x, self.y, self.z])

    def length(self):
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero vector.")
        return Vector3(self.x / length, self.y / length, self.z / length)

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"


class Matrix4:
    def __init__(self, values=None):
        if values is None:
            self.values = np.eye(4)  # Инициализация единичной матрицы 4x4
        else:
            self.values = np.array(values)

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            return Matrix4(np.dot(self.values, other.values))
        elif isinstance(other, Vector3):
            # Умножение матрицы на вектор
            vec = np.array([other.x, other.y, other.z, 1])  # Преобразуем вектор в однородные координаты
            result = np.dot(self.values, vec)  # Умножаем матрицу на вектор
            return Vector3(result[0], result[1], result[2])  # Возвращаем новый вектор
        else:
            raise TypeError("Unsupported operand type(s) for *: 'Matrix4' and '{}'".format(type(other).__name__))

    @staticmethod
    def translation(tx, ty, tz):
        return Matrix4([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_x(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return Matrix4([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_y(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return Matrix4([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_z(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return Matrix4([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def scaling(sx, sy, sz):
        return Matrix4([
            [sx, 0, 0, 0],
            [0, sy , 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

    def __repr__(self):
        return f"Matrix4({self.values})"