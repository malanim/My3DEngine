# vector.py

import math

class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / length, self.y / length, self.z / length)

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

class Matrix4:
    def __init__(self, values=None):
        if values is None:
            self.values = [[0] * 4 for _ in range(4)]
        else:
            self.values = values

    def __mul__(self, other):
        result = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                result[i][j] = sum(self.values[i][k] * other.values[k][j] for k in range(4))
        return Matrix4(result)

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
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix4([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_y(angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix4([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_z(angle):
        c = math.cos(angle)
        s = math.sin(angle)
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
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

    def __repr__(self):
        return f"Matrix4({self.values})"

# Тестирование vector.py
# if __name__ == "__main__":
#     # Тестирование Vector3
#     v1 = Vector3(1, 2, 3)
#     v2 = Vector3(4, 5, 6)
#     print("v1 + v2 =", v1 + v2)
#     print("v1 - v2 =", v1 - v2)
#     print("v1 * 2 =", v1 * 2)
#     print("Длина v1 =", v1.length())
#     print("Нормализованный v1 =", v1.normalize())

#     # Тестирование Matrix4
#     m1 = Matrix4.translation(1, 2, 3)
#     m2 = Matrix4.rotation_x(math.pi / 4)
#     m3 = m1 * m2
#     print("Результат умножения матриц =", m3)

# Результаты тестов:
# v1 + v2 = Vector3(5, 7, 9)
# v1 - v2 = Vector3(-3, -3, -3)
# v1 * 2 = Vector3(2, 4, 6)
# Длина v1 = 3.7416573867739413
# Нормализованный v1 = Vector3(0.2672612419124244, 0.5345224838248488, 0.8017837257372732)
# Результат умножения матриц = Matrix4([[1, 0.0, 0.0, 1], [0, 0.7071067811865476, -0.7071067811865476, 2], [0, 0.7071067811865476, 0.7071067811865476, 3], [0, 0.0, 0.0, 1]])