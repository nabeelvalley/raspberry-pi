from picamera import PiCamera
from time import sleep, time

def full_image_path(filename: str) -> str:
    """
    Get full path for image file given the file name
    """
    pictures_root = '/home/pi/Pictures/'
    return pictures_root + filename
    

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
    camera = configure_camera()
    filename = str(time()) + '.jpg'
    image_path = full_image_path(filename)
    camera.capture(image_path)
    print('Image saved to ' + image_path)

if __name__ == '__main__':
    take_picture()