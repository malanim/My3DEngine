# main.py

from renderer import Renderer
from object import Cube, Sphere, Plane
from light import Light  # Импортируем класс Light
from camera import Camera  # Импортируем класс Camera
from vector import Vector3, Matrix4  # Импортируем класс Vector3
from time import sleep

def main():
    # Инициализация объектов
    obj = Cube(size=1, color=(100, 100, 255))
    objects = [obj]

    # Создаем матрицу трансляции
    translation_matrix = Matrix4.translation(2, -2, 0)  # Перемещение на 2 по X и -2 по Y
    # Применяем трансляцию к объекту
    obj.transform(translation_matrix)
    
    # Инициализация источников света
    lights = [Light(position=Vector3(5, 5, 5), color=(255, 255, 255))]

    # Инициализация камеры
    camera = Camera(position=Vector3(0, 0, -5), direction=Vector3(0, 0, -1), up_vector=Vector3(0, 1, 0))

    # Инициализация рендерера
    renderer = Renderer()

    rotation_angle = 0  # Угол вращения
    rotation_angle += 0.05  # Увеличиваем угол вращения

    while True:
        
        rotation_matrix = Matrix4.rotation_z(rotation_angle)  # Создаем матрицу вращения вокруг оси Y
        
        # Применяем матрицу вращения к кубу
        obj.transform(rotation_matrix)

        # Рендерим сцену
        renderer.render(objects, camera, lights)
        input()  # Ожидание ввода от пользователя
        sleep(0.01)  # Задержка для управления скоростью отображения

if __name__ == "__main__":
    main()