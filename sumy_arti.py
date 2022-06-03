import random
import requests
from newspaper import Article
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
from wand.color import Color
from wand.font import Font
from wand.image import Image
from constants import *
from utils import filter_images, get_highquality_image

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

# ideal Height, ideal Width
dims = (1080, 1920)
ideal_aspect = dims[0] / dims[1]


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
with Image(blob=image_blob.content) as canvas:
    canvas.crop(*resize[0])
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
    canvas.save(filename="assets/images/text_overlayed_1.jpg")

with Image(blob=image_blob.content) as canvas:
    canvas.crop(*resize[1])
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
    canvas.save(filename="assets/images/text_overlayed_2.jpg")

# TODO: Posting the Story on Instagram manually (not using the API)
def main():
    filter_images(images_URLs)

