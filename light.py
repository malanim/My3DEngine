# light.py

class Light:
    def __init__(self, position, color):
        self.position = position  # Позиция источника света (объект Vector3)
        self.color = color        # Цвет источника света (RGB)