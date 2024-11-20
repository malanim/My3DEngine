# test_camera.py

from camera import Camera
from vector import Vector3
import numpy as np

# Пример теста для класса Camera
def test_camera():
    # Создание камеры с корректными параметрами
    camera = Camera(Vector3(0, 0, 0), Vector3(0, 0, -1), Vector3(0, 1, 0))

    # Проверка начальных значений
    # assert np.array_equal(camera.position, np.array([0, 0, 0])), "Ошибка: Неверная позиция камеры"
    # assert np.array_equal(camera.direction, np.array([0, 0, -1])), "Ошибка: Неверное направление камеры"
    # assert np.array_equal(camera.up_vector, np.array([0, 1, 0])), "Ошибка: Неверный вверх-вектор"

    # Отладочные сообщения перед выводом матрицы
    print("Текущая позиция камеры:", camera.position)
    print("Текущее направление камеры:", camera.direction)
    print("Текущий вверх-вектор камеры:", camera.up_vector)
    # Получение матрицы вида
    view_matrix = camera.get_view_matrix()
    print("Матрица вида:")
    print(view_matrix)

    # Обновление позиции и направления
    camera.update(Vector3(1, 1, 1), Vector3(0, 0, -1))

    # Проверка обновленных значений
    # assert np.array_equal(camera.position, np.array([1, 1, 1])), "Ошибка: Неверная обновленная позиция камеры"
    # assert np.array_equal(camera.direction, np.array([0, 0, -1])), "Ошибка: Неверное обновленное направление камеры"

    # Отладочные сообщения перед выводом матрицы
    print("Текущая позиция камеры:", camera.position)
    print("Текущее направление камеры:", camera.direction)
    print("Текущий вверх-вектор камеры:", camera.up_vector)
    # Получение матрицы вида
    view_matrix = camera.get_view_matrix()
    print("Матрица вида:")
    print(view_matrix)

    # Тестирование с нулевыми векторами
    # try:
    #     camera_with_zero_direction = Camera(Vector3(0, 0, 0), Vector3( 0, 0, 0), Vector3(0, 1, 0))
    # except ValueError as e:
    #     print(f"Ошибка при создании камеры с нулевым направлением: {e}")

    # try:
    #     camera_with_zero_up = Camera(Vector3(0, 0, 0), Vector3(0, 0, -1), Vector3(0, 0, 0))
    # except ValueError as e:
    #     print(f"Ошибка при создании камеры с нулевым вверх-вектором: {e}")

# Запуск теста
if __name__ == "__main__":
    test_camera()