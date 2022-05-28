import requests
from newspaper import Article
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
from wand.font import Font

article_URL = "https://www.wired.com/story/researchers-made-ultracold-quantum-bubbles-on-the-space-station/"

# image_URL = "https://media.wired.com/photos/628d7932616e0f74943c26c4/master/w_120,c_limit/cal-cygnus-scaled-science.jpg"
image_URL = "https://i.imgur.com/YobrZ8r.png"


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


CAPTION, images_URLs = parse_summerize_article(article_URL)

assert CAPTION


image_blob = requests.get(image_URL)

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
    img.save(filename='assets/images/cropped_1.jpg')

with Image(blob=image_blob.content) as img:
    img.crop(*resize[1])
    img.save(filename='assets/images/cropped_2.jpg')


with Image(blob=image_blob.content) as canvas:
    canvas.crop(*resize[0])
    canvas.font = Font("assets/fonts/Roboto-Regular.ttf",
                       size=53,
                       color=Color('white'))
    caption_width = int(canvas.width/1.2)
    margin_left = int((canvas.width-caption_width)/2)
    margin_top = int(30)
    canvas.caption(CAPTION[0], gravity='north',
                   width=caption_width, left=margin_left,
                   top=margin_top)
    canvas.format = "jpg"
    canvas.save(filename='assets/images/text_overlayed_1.jpg')

with Image(blob=image_blob.content) as canvas:
    canvas.crop(*resize[1])
    canvas.font = Font("assets/fonts/Roboto-Regular.ttf",
                       size=53,
                       color=Color('white'))
    caption_width = int(canvas.width/1.2)
    margin_left = int((canvas.width-caption_width)/2)
    margin_top = int(30)
    canvas.caption(CAPTION[1], gravity='north',
                   width=caption_width, left=margin_left,
                   top=margin_top)
    canvas.format = "jpg"
    canvas.save(filename='assets/images/text_overlayed_2.jpg')


# TODO: Posting the Story on Instagram manually (not using the API)
