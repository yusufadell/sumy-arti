# Python3 program to Filtering Images
# based on Size Attributes
import datetime
import os
import os.path
import shutil

import requests
from PIL import Image


def filterImages(images_URL, thresholdWidth, thresholdHeight):

    # Defining images array for
    # identifying only image files
    valid_images = (".jpg", ".gif", ".png", ".tga",
                    ".jpeg", ".PNG", ".JPG", ".JPEG")
    imgs_URLs = [img for img in images_URL if img.endswith(valid_images)]
    imgs_PATH = "assets/tmp/"

    # download valid_images image from url and save it to disk
    for url in imgs_URLs:
        prefix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        basename = url.split('/')[-1]
        filename = "_".join([prefix, basename])
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(imgs_PATH + filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            print('Error downloading image')

    # get all the images in the folder
    imgs = [imgs_PATH + f for f in os.listdir(imgs_PATH) if f.endswith(".jpg")]

    # iterate over all the images
    for img in imgs:
        try:
            # open the image
            im = Image.open(img)
            # get the image size
            width, height = im.size

            # check the image size
            if width >= thresholdWidth and height >= thresholdHeight:
                # if the image size satisfies the requirements,
                # save it in the destination folder
                shutil.copyfile(img, imgs_PATH + os.path.basename(img))
                print('satisfy the requirement => ' + img)
            else:
                # if the image size does not satisfy the requirements,
                print('Does not satisfy the requirement => ' + img)
                os.remove(img)
        except IOError:
            print('Cannot open image: ' + img)


urls = ['https://media.wired.com/photos/628d7932616e0f74943c26c4/master/w_2560%2Cc_limit/cal-cygnus-scaled-science.jpg',
        'https://www.wired.com/verso/static/wired/assets/logo-reverse.548f3a7478ee71f618044082aa222dd05f31249c.svg',
        'https://media.wired.com/photos/628d7932616e0f74943c26c4/191:100/w_1280,c_limit/cal-cygnus-scaled-science.jpg',
        'https://www.wired.com/verso/static/wired/assets/logo-header.a7598835a549cb7d5ce024ef0710935927a034f9.svg',
        'https://www.wallpapermaiden.com/image/2016/09/02/google-logo-opening-doors-colorful-stripes-technology-5335.jpg']


filterImages(1000, 1000)
