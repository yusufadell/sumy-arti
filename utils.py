# Python3 program to Filtering Images
# based on Size Attributes
import random
import shutil
import uuid
from pathlib import Path

import requests
from PIL import Image

from constants import *


def filter_images(images_URL, tmp_images_path=tmp_img_path, image_path=filtered_image_path, thresholdWidth=thresholdWidth, thresholdHeight=thresholdHeight):
    _ = download_imagesURL(images_URL, tmp_images_path)
    path = handle_dir_creation(image_path)
    # iterate over all the images
    for img in _:
        try:
            # open the image
            im = Image.open(img)
            # get the image size
            width, height = im.size

            # check the image size
            if width >= thresholdWidth and height >= thresholdHeight:
                # if the image size satisfies the requirements,
                # save it in the destination folder

                shutil.copyfile(img.absolute(), path / img.name)
                print(f"satisfy the requirement => {img}")
            else:
                # if the image size does not satisfy the requirements,
                print(f"Does not satisfy the requirement => {img}")
                img.unlink()
        except IOError:
            print(f"Cannot open image: {img}")
