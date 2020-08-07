from picamera import PiCamera
from time import sleep, time
from os import path, getcwd

def full_image_path(filename: str) -> str:
    """
    Get full path for a file to be palced in the `out` directory given the file name
    """
    working_dir = path.abspath(getcwd())
    file_path = path.join(working_dir, 'out', filename)
    return file_path
    

def configure_camera() -> PiCamera:
    """
    Create a PiCamera instance, let the camera warm up, then returns the PiCamera instance
    Also rotates the camera because my placement is currently upside-down
    """
    camera = PiCamera()
    camera.rotation = 180

    sleep(2.5)

    return camera

def take_picture() -> None:
    """
    Take a picture using the current unix time as the file name
    """
    filename = str(time()) + '.jpg'
    image_path = full_image_path(filename)
    
    configure_camera().capture(image_path)

    print('Image saved to ' + image_path)

if __name__ == '__main__':
    take_picture()