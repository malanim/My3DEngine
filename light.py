from vector import Vector3

class Light:
    def __init__(self, position, color, intensity=1.0, attenuation=(1.0, 0.09, 0.032)):
        self.position = position      # Позиция источника света (объект Vector3)
        self.color = color           # Цвет источника света (RGB)
        self.intensity = intensity   # Базовая интенсивность света
        # Коэффициенты затухания света (константный, линейный, квадратичный)
        self.attenuation = attenuation
    
    def calculate_attenuation(self, distance):
        """Вычисляет затухание света на основе расстояния до точки."""
        constant, linear, quadratic = self.attenuation
        # Улучшенная формула затухания с ограничением минимального значения
        attenuation = 1.0 / (constant + linear * distance + quadratic * distance * distance)
        return max(0.1, min(1.0, attenuation))  # Ограничиваем значения между 0.1 и 1.0
        
    def copy_position(self):
        """Returns a copy of the light's position vector."""
        return Vector3(self.position.x, self.position.y, self.position.z)