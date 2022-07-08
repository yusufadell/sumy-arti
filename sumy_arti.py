import os
import random

import requests
from newspaper import Article
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from wand.color import Color
from wand.font import Font
from wand.image import Image

from constants import *
from utils import filter_images
from utils import get_highquality_image

chosen_image = get_highquality_image()


def parse_summerize_article(url):
    """parse_summerize_article parse_summerize_article parses a given URL and returns a summary

    :param url: article URL to parse and summarize
    :type url: string
    :return: list object with SENTENCES_COUNT number of sentences from the article summary
    :rtype: list
    """
    article = Article(url)
    article.download()
    article.parse()

    LANGUAGE = "english"
    SENTENCES_COUNT = 10

    parser = PlaintextParser.from_string(article.text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)

    return [
        sentence._text
        for sentence in summarizer(parser.document, SENTENCES_COUNT)
    ], list(article.images)


CAPTION, images_URLs = parse_summerize_article(article_URL)
assert CAPTION

with Image(filename=chosen_image) as img:
    size = img.size

width = size[0]
height = size[1]
aspect = width / height


def crop_edges(ideal_aspect, width, height):
    """crop_edges crops the image to the ideal aspect ratio

    :param ideal_aspect: ideal aspect ratio for the image
    :type ideal_aspect: float
    :param width: width of the image
    :type width: int
    :param height: height of the image
    :type height: int
    :return: list of tuples with the coordinates to crop the image
    :rtype: list
    """
    new_width = int(height * ideal_aspect)
    resize = (
        (0, 0, int(new_width), int(height)),
        (int(width - new_width), 0, int(width), int(height)),
    )

    return resize


def crop_top_bottom(ideal_aspect, width, height):
    """crop_top_bottom _summary_crop_top_bottom crops the image to the ideal aspect ratio

    :param ideal_aspect: ideal aspect ratio for the image
    :type ideal_aspect: float
    :param width: width of the image
    :type width: int
    :param height: height of the image
    :type height: int
    :return: list of tuples with the coordinates to crop the image
    :rtype: list
    """
    new_height = int(width / ideal_aspect)
    resize = (
        (0, 0, int(width), int(new_height)),
        (0, int(height - new_height), int(width), int(height)),
    )

    return resize


def crop_image_handler(aspect, width, height):
    """crop_image_handler _summary_crop_image_handler crops the image to the ideal aspect ratio

    :param aspect: ideal aspect ratio for the image
    :type aspect: float
    :param width: width of the image
    :type width: int
    :param height: height of the image
    :type height: int
    :return: list of tuples with the coordinates to crop the image
    :rtype: list
    """
    if aspect > ideal_aspect:
        return crop_edges(ideal_aspect, width, height)
    else:
        return crop_top_bottom(ideal_aspect, width, height)


resize = crop_image_handler(aspect, width, height)
assert resize

with Image(filename=chosen_image) as img:
    img.crop(*resize[0])

    img.save(filename="assets/images/cropped_1.jpg")

with Image(filename=chosen_image) as img:
    img.crop(*resize[1])
    img.save(filename="assets/images/cropped_2.jpg")


# Overlay text from CAPTION on the image and save.
def overlay_text(CAPTION, filename, resize, image_path):
    with Image(filename=filename) as canvas:
        canvas.crop(*resize)
        canvas.font = Font("assets/fonts/Roboto-Regular.ttf",
                           size=53,
                           color=Color("white"))
        caption_width = int(canvas.width / 1.2)
        margin_left = int((canvas.width - caption_width) / 2)
        margin_top = int(30)
        canvas.caption(
            random.choice(CAPTION),
            gravity="north",
            width=caption_width,
            left=margin_left,
            top=margin_top,
        )
        canvas.format = "jpg"
        canvas.save(filename=image_path)


overlay_text(CAPTION, chosen_image, resize[0], image1_path)  # crop_edges
overlay_text(CAPTION, chosen_image, resize[1], image2_path)  # crop_top_bottom


def upload_to_instagram(image_path):
    """upload_to_instagram _summary_upload_to_instagram uploads the image to instagram
    :param image_path: path to the image
    :type image_path: string
    :return: None
    :rtype: None
    """
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    image_name = image_path.split("/")[-1]
    upload_url = "https://api.instagram.com/v1/media/upload"
    payload = {"access_token": os.environ.get("INSTAGRAM_ACCESS_TOKEN")}
    files = {"photo": image_data}
    response = requests.post(upload_url, data=payload, files=files)
    if response.status_code == 200:
        # extract the image id
        image_id = response.json()["data"]["id"]
        # post the image to an account
        post_url = "https://api.instagram.com/v1/media/{}/comments".format(
            image_id)
        payload = {
            "access_token":
            os.environ.get("INSTAGRAM_ACCESS_TOKEN"),
            "text":
            "Thank you for reading this article. I hope you enjoyed it. #wired #cygnus #quantum #space #science",
        }
        response = requests.post(post_url, data=payload)
        if response.status_code == 200:
            print("Image uploaded successfully")
        else:
            print("Something went wrong when uploading the image")
    else:
        print("Something went wrong when uploading the image")


def main():
    filter_images(images_URLs)
