# engine.py
from renderer import Renderer
from camera import Camera
from vector import Vector3
class Engine:
    def __init__(self):
        self.objects = []
        self.lights = []

    def add_object(self, obj):
        self.objects.append(obj)

    def add_light(self, light):
        self.lights.append(light)

    def update(self):
        # Логика обновления состояния игры
        pass

    def render(self):
        renderer = Renderer()
        camera = Camera(position=Vector3(0, 0, -5), direction=Vector3(0, 0, -1), up_vector=Vector3(0, 1, 0))
        renderer.render(self.objects, camera, self.lights)