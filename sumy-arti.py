from newspaper import Article
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
from wand.image import Image
import requests

url = "https://www.wired.com/story/researchers-made-ultracold-quantum-bubbles-on-the-space-station/"
article = Article(url)
article.download()
article.parse()

LANGUAGE = "english"
SENTENCES_COUNT = 10

parser = PlaintextParser.from_string(article.text, Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)

CAPTION = [sentence._text for sentence in summarizer(
    parser.document, SENTENCES_COUNT)]

print(CAPTION)

image_url = 'https://media.wired.com/photos/628d7932616e0f74943c26c4/master/w_120,c_limit/cal-cygnus-scaled-science.jpg'
image_blob = requests.get(image_url)
with Image(blob=image_blob.content) as img:
    print(img.size)

dims = (1080, 1920)
ideal_width = dims[0]
ideal_height = dims[1]
ideal_aspect = ideal_width / ideal_height

with Image(blob=image_blob.content) as img:
    size = img.size

width = size[0]
height = size[1]
aspect = width/height

if aspect > ideal_aspect:
    # crop the left and right edges:
    new_width = int(ideal_aspect * height)
    offset = (width - new_width) / 2
    resize = (
        (0, 0, int(new_width), int(height)),
        (int(width-new_width), 0, int(width), int(height))
    )
else:
    # crop the top and bottom edges:
    new_height = int(width / ideal_aspect)
    offset = (height - new_height) / 2
    resize = (
        (0, 0, int(width), int(new_height)),
        (0, int(height-new_height), int(width), int(height))
    )

with Image(blob=image_blob.content) as img:
    img.crop(*resize[0])
    img.save(filename='cropped_1.jpg')
    

with Image(blob=image_blob.content) as img:
    img.crop(*resize[1])
    img.save(filename='cropped_2.jpg')