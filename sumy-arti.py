import requests
from newspaper import Article
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
from wand.image import Image

article_URL = "https://www.wired.com/story/researchers-made-ultracold-quantum-bubbles-on-the-space-station/"
image_URL = "https://media.wired.com/photos/628d7932616e0f74943c26c4/master/w_120,c_limit/cal-cygnus-scaled-science.jpg"


def parse_summerize_article(url):
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
    ]


CAPTION = parse_summerize_article(article_URL)
assert CAPTION


def get_image_blob(url):
    return requests.get(image_URL)


image_blob = get_image_blob(image_URL)

with Image(blob=image_blob.content) as img:
    size = img.size

width = size[0]
height = size[1]
aspect = width / height

# ideal Height, ideal Width
dims = (1080, 1920)
ideal_aspect = dims[0] / dims[1]


def crop_edges(ideal_aspect, width, height):
    # crop the left and right edges:
    new_width = int(ideal_aspect * height)
    resize = (
        (0, 0, int(new_width), int(height)),
        (int(width - new_width), 0, int(width), int(height)),
    )
    return resize


def crop_top_bottom(ideal_aspect, width, height):
    new_height = int(width / ideal_aspect)
    resize = (
        (0, 0, int(width), int(new_height)),
        (0, int(height - new_height), int(width), int(height)),
    )

    return resize


def crop_image_handler(aspect, width, height):
    if aspect > ideal_aspect:
        return crop_edges(ideal_aspect, width, height)
    else:
        return crop_top_bottom(ideal_aspect, width, height)


resize = crop_image_handler(aspect, width, height)
assert resize

with Image(blob=image_blob.content) as img:
    img.crop(*resize[0])
    img.save(filename="assets/cropped_1.jpg")

with Image(blob=image_blob.content) as img:
    img.crop(*resize[1])
    img.save(filename="assets/cropped_2.jpg")
