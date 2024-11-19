# test_object.py

from object import Cube, Plane, Sphere, Cylinder  # Импортируем новые классы
from vector import Vector3
from pprint import pprint

# Тестирование класса Cube
cube = Cube(size=2, color=(255, 0, 0))
print("Вершины куба:")
pprint(cube.vertices)
print("Грани куба:")
pprint(cube.faces)

# Тестирование класса Plane
plane = Plane(width=2, height=2, color=(0, 255, 0))
print("\nВершины плоскости:")
pprint(plane.vertices)
print("Грани плоскости:")
pprint(plane.faces)

# Тестирование класса Sphere
sphere = Sphere(radius=1, color=(0, 0, 255), segments=12)
print("\nВершины сферы:")
pprint(sphere.vertices)
print("Грани сферы:")
pprint(sphere.faces)

# Тестирование класса Cylinder
cylinder = Cylinder(radius=1, height=2, color=(255, 255, 0), segments=12)
print("\nВершины цилиндра:")
pprint(cylinder.vertices)
print("Грани цилиндра:")
pprint(cylinder.faces)