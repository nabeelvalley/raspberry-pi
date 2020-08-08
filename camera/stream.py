# From https://blog.miguelgrinberg.com/post/video-streaming-with-flask

from camera.pi_camera import Camera

import io
from time import sleep
from threading import Condition
from flask import Response

def gen(camera: Camera):
    """
    Video streaming generator function.
    """
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def as_http_response():
    """
    Get Generated Stream as a Multipart HTTP Response
    """
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
