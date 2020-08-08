from os import getcwd
from os import path

from zipfile import ZipFile

import tflite_runtime as tf

from urllib.request import urlretrieve

model_url = 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip'

model_filename = 'coco-model.zip'
model_dirname = 'coco-model'

def does_file_exist(filepath: str) -> bool:
    """
    Check if the given filepath exists
    """
    return path.isfile(filepath)

def unzip(filepath: str, outdir: str):
    """
    Unzip the given file and output as the out dir
    """
    with ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(outdir)

def download_model():
    """
    Download a TF Mode, and extract it into the relevant directory
    """
    working_dir = path.abspath(getcwd())
    filepath = path.join(working_dir, 'out', model_filename)
    outdir = path.join(working_dir, 'out', model_dirname)

    if not does_file_exist(filepath):
        urlretrieve(model_url, filepath)
        unzip(filepath, outdir)
    else:
        print("File already exists, not downloading")

if __name__ == '__main__':
    download_model()