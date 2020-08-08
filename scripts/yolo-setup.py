import tensorflow as tf
import os

ROOT = os.path.join(os.getcwd(),'out')

filename_darknet_weights = tf.keras.utils.get_file(
    os.path.join(ROOT,'yolov3.weights'),
    origin='https://pjreddie.com/media/files/yolov3-tiny.weights')

TINY = True

filename_convert_script = tf.keras.utils.get_file(
    os.path.join(ROOT,'convert.py'),
    origin='https://raw.githubusercontent.com/zzh8829/yolov3-tf2/master/convert.py')

filename_classes = tf.keras.utils.get_file(
    os.path.join(ROOT,'coco.names'),
    origin='https://raw.githubusercontent.com/zzh8829/yolov3-tf2/master/data/coco.names')

filename_converted_weights = os.path.join(ROOT,'yolov3.tf')

print("Now that this is all done, I need you to run the following:")

print(f'python3 "{filename_convert_script}" --weights "{filename_darknet_weights}" --output "{filename_converted_weights}" --tiny')
