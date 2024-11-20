# main.py

from camera import Camera
from renderer import Renderer
from object import Cube, Sphere, Plane  # Импортируйте ваши классы объектов
from vector import Vector3, Color, Matrix4  # Импортируйте класс Color

def main():
    # Создайте камеру
    camera = Camera(Vector3(0, 0, 0), Vector3(0, 0, -1), Vector3(0, 1, 0))

    # Создайте рендерер
    renderer = Renderer()

    # Создайте некоторые 3D-объекты с цветами
    objects = [
        Cube(size=2, color=Color(255, 0, 0)),  # Красный куб
        Sphere(radius=1, color=Color(0, 255, 0), segments=12),  # Зеленая сфера
        Plane(width=3, height=3, color=Color(0, 0, 255)),  # Синяя плоскость
    ]

    # Основной цикл игры
    angle = 0  # Угол вращения
    while True:
        # Обновление состояния игры (например, ввод, движение объектов и т.д.)
        angle += 0.01  # Увеличиваем угол для вращения
        rotation_matrix = Matrix4.rotation_y(angle)  # Создаем матрицу вращения вокруг оси Y

        for obj in objects:
            obj.transform(rotation_matrix)  # Применяем матрицу вращения к объекту

        # Рендеринг объектов
        renderer.render(objects, camera)
        input()

if __name__ == "__main__":
    main()