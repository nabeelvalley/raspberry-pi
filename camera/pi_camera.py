# From https://github.com/miguelgrinberg/flask-video-streaming/blob/master/camera_pi.py

import io
from time import sleep
from picamera import PiCamera
from camera.base_camera import BaseCamera

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with PiCamera(resolution='640x480', framerate=16) as camera:
            camera.rotation = 180
            # let camera warm up
            sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
