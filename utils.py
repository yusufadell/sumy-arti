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


def download_imagesURL(images_URL, tmp_images_path):
    # Defining images array for
    # identifying only image files
    imgs_URLs = [img for img in images_URL if img.endswith(valid_images)]
    # download valid_images image from url and save it to disk
    tmp_path = handle_dir_creation(tmp_images_path)

    for url in imgs_URLs:
        filename = uniqe_name(url)
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            # Try dir creation
            with open(tmp_path / filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            print("Error downloading image")

    # return the list of images downloaded
    return [f for f in tmp_path.iterdir() if f.name.endswith(valid_images)]


def handle_dir_creation(path):
    p = Path(path)
    try:
        p.mkdir(parents=True, exist_ok=True)
    except OSError:
        print(f"Creation of the directory {path} failed")
    else:
        print(f"Successfully created the directory {path} ")
    return p


def uniqe_name(url):
    unique_imagename = str(uuid.uuid4())
    basename = url.split("/")[-1]
    filename = "_".join([unique_imagename, basename])
    return filename


def get_highquality_image(image_path=filtered_image_path):
    path = handle_dir_creation(image_path)
    # check if dir is empty
    images = list(path.absolute().iterdir())
    return backup_image if len(images) == 0 else random.choice(images)


