# main.py

from renderer import Renderer
from object import Cube, Sphere, Plane
from light import Light
from camera import Camera
from vector import Vector3, Matrix4
from time import sleep

def create_scene():
    """Create a scene with multiple objects and light sources"""
    # Initialize objects
    objects = [
        Cube(size=1.5, color=(255, 100, 100)),  # Red cube
        Cube(size=1.5, color=(100, 255, 100)),  # Green cube
        Cube(size=1.5, color=(100, 100, 255)),  # Blue cube
        Cube(size=1.5, color=(255, 255, 100))   # Yellow cube
    ]
    
    # Position objects
    translations = [
        Matrix4.translation(-3, 0, 3),  # Left
        Matrix4.translation(3, 0, 3),   # Right
        Matrix4.translation(0, 3, 3),   # Top
        Matrix4.translation(0, -3, 3)   # Bottom
    ]
    
    for obj, trans in zip(objects, translations):
        obj.transform(trans)
    
    # Initialize lights with different colors
    lights = [
        Light(Vector3(-5, 3, 0), color=(255, 100, 100)),  # Red light
        Light(Vector3(5, 3, 0), color=(100, 255, 100)),   # Green light
        Light(Vector3(0, 5, 0), color=(100, 100, 255))    # Blue light
    ]
    
    # Initialize camera
    camera = Camera(
        position=Vector3(0, 0, -10),
        direction=Vector3(0, 0, 1),
        up_vector=Vector3(0, 1, 0),
        projection_type="perspective",
        fov=90,
        near=0.1,
        far=100
    )
    
    return objects, lights, camera

def update_objects(objects, time):
    """Update object rotations"""
    for i, obj in enumerate(objects):
        # Reset object vertices
        obj.vertices = Cube(size=1.5, color=obj.color).vertices
        
        # Apply unique rotation to each object
        rotation = Matrix4.rotation_y(time * 0.5 * (i + 1))
        rotation = rotation @ Matrix4.rotation_x(time * 0.3 * (i + 1))
        obj.transform(rotation)
        
        # Reapply position
        translations = [
            Matrix4.translation(-3, 0, 3),
            Matrix4.translation(3, 0, 3),
            Matrix4.translation(0, 3, 3),
            Matrix4.translation(0, -3, 3)
        ]
        obj.transform(translations[i])

def main():
    objects, lights, camera = create_scene()
    renderer = Renderer()
    time = 0
    projection_toggle = True
    while True:
        # Handle projection toggle
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'p':
                projection_toggle = not projection_toggle
                camera.projection_type = "perspective" if projection_toggle else "orthographic"
                print(f"Switched to {camera.projection_type} projection")

        # Update object rotations
        time += 0.01
        update_objects(objects, time)

        # Render the scene
        renderer.render(objects, camera, lights)
        input()  # Ожидание ввода от пользователя
        sleep(0.001)  # Задержка для управления скоростью отображения

if __name__ == "__main__":
    main()