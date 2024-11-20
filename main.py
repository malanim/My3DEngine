# main.py

from renderer import Renderer
from object import Cube, Sphere, Plane
from light import Light  # Импортируем класс Light
from camera import Camera  # Импортируем класс Camera
from vector import Vector3, Matrix4  # Импортируем класс Vector3
from time import sleep

def main():
    # Инициализация объектов
    obj = Cube(size=2, color=(100, 100, 255))  # Увеличим размер куба
    objects = [obj]

    # Создаем матрицу трансляции - поместим объект перед камерой
    translation_matrix = Matrix4.translation(0, 0, 3)  # Перемещение вперед по Z
    # Применяем трансляцию к объекту
    obj.transform(translation_matrix)
    
    # Инициализация источников света
    lights = [Light(position=Vector3(5, 5, 5), color=(255, 255, 255))]

    # Инициализация камеры с перспективной проекцией
    camera = Camera(
        position=Vector3(0, 0, -3),
        direction=Vector3(0, 0, 1),
        up_vector=Vector3(0, 1, 0),
        projection_type="perspective",
        fov=90,
        near=0.1,
        far=100
    )

    # Инициализация рендерера
    renderer = Renderer()

    rotation_angle = 0  # Угол вращения

    projection_toggle = True  # True для перспективы, False для ортографии
    while True:
        # Обработка клавиши P для переключения проекции
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'p':
                projection_toggle = not projection_toggle
                camera.projection_type = "perspective" if projection_toggle else "orthographic"
                print(f"Switched to {camera.projection_type} projection")

        rotation_angle += 0.05  # Увеличиваем угол вращения
        
        # Сбрасываем позицию объекта
        obj.vertices = Cube(size=1, color=(100, 100, 255)).vertices
        
        # Применяем последовательно трансформации
        rotation_matrix = Matrix4.rotation_y(rotation_angle)  # Вращение вокруг Y
        obj.transform(rotation_matrix)
        obj.transform(translation_matrix)  # Затем перемещение

        # Рендерим сцену
        renderer.render(objects, camera, lights)
        # input()  # Ожидание ввода от пользователя
        sleep(0.01)  # Задержка для управления скоростью отображения

if __name__ == "__main__":
    main()