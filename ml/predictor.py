# Adapted from https://github.com/tensorflow/examples/blob/master/lite/examples/object_detection/raspberry_pi/detect_picamera.py

import numpy as np
from tflite_runtime.interpreter import Interpreter

from io import BytesIO
import re
import time

from PIL import Image, ImageDraw

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

def load_labels(path):
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels

def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor

def detect_objects(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results

def annotate_objects(annotator, results, labels):
  """Draws the bounding box and label for each object in the results."""
  for obj in results:
    # Convert the bounding box figures from relative coordinates
    # to absolute coordinates based on the original resolution
    ymin, xmin, ymax, xmax = obj['bounding_box']
    xmin = int(xmin * CAMERA_WIDTH)
    xmax = int(xmax * CAMERA_WIDTH)
    ymin = int(ymin * CAMERA_HEIGHT)
    ymax = int(ymax * CAMERA_HEIGHT)

    # Overlay the box, label, and score on the camera preview
    annotator.bounding_box([xmin, ymin, xmax, ymax])
    annotator.text([xmin, ymin],
                   '%s\n%.2f' % (labels[obj['class_id']], obj['score']))


class Predictor():
    def __init__(self, modelpath: str, labelpath:str) -> None:

        self.modelpath = modelpath
        
        self.labels = load_labels(labelpath)
        self.labelpath = labelpath
        
        # Load the TFLite model and allocate tensors.
        self.interpreter = Interpreter(modelpath)
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, frame):
        if frame:
            _, input_height, input_width, _ = self.interpreter.get_input_details()[0]['shape']

            bytes_io = BytesIO()
            bytes_io.write(frame)

            with Image.open(bytes_io).convert('RGB').resize((input_width, input_height), Image.ANTIALIAS) as image:

              result = detect_objects(self.interpreter, image, 0.5)

              draw = ImageDraw.Draw(image)
              for r in result:
                  description = self.labels[int(r['class_id'])]

                  ymin, xmin, ymax, xmax = r['bounding_box']

                  shape = [
                      int(xmin * CAMERA_WIDTH),
                      int(xmax * CAMERA_WIDTH),
                      int(ymin * CAMERA_HEIGHT),
                      int(ymax * CAMERA_HEIGHT)
                  ]

                  draw.rectangle(shape, outline ="red")

                  text_pos = ((xmin + xmax) * CAMERA_WIDTH * 0.5, (ymin + ymax) * CAMERA_HEIGHT * 0.5 )

                  draw.text(text_pos, description, fill="red")

              out_io= BytesIO()  
              image.save(out_io, 'jpeg')
              out_io.seek(0)

              outbytes = out_io.read()
              
              return outbytes
        else:
            return frame