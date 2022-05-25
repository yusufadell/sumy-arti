from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
from sumy.nlp.tokenizers import Tokenizer

from sumy.nlp.stemmers import Stemmer
from newspaper import Article

url = "https://www.wired.com/story/researchers-made-ultracold-quantum-bubbles-on-the-space-station/"
article  =  Article(url)
article.download()
article.parse()

LANGUAGE = "english"
SENTENCES_COUNT = 10

parser = PlaintextParser.from_string(article.text, Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)

CAPTION = []
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    CAPTION.append(sentence._text)

print(CAPTION)
