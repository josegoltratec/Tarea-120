from flask import Flask, render_template, request
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

app = Flask(__name__)

def get_lang(text):
    nlp = spacy.load("en_core_web_sm")
    Language.factory("language_detector", func=get_lang_detector)
    nlp.add_pipe('language_detector', last=True)
    doc = nlp(text)

    return doc._.language


def get_lang_detector(nlp, name):
    return LanguageDetector()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/process", methods=['POST'])
def process():
    results = []
    num_of_results = 0

    if request.method == 'POST':
        rawtext = request.form.get('rawtext')
        taskOption = request.form.get('taskoption')

        if taskOption == "organization":
            labels = ["ORG"]
        elif taskOption == "person":
            labels = ["PER"]
        elif taskOption == "money":
            labels = ["MONEY"]
        elif taskOption == "product":
            labels = ["PRODUCT"]
        elif taskOption == "geolocation":
            labels = ["GPE"]
        else:
            labels = ["ORG", "PER", "MONEY", "PRODUCT", "GPE"]

        lang = get_lang(rawtext)['language']
        print(lang)

        if lang == 'en':
            nlp = spacy.load("en_core_web_sm")
        elif lang == 'es':
            nlp = spacy.load("es_core_news_sm")
        else:
            nlp = spacy.load("en_core_web_sm")

        doc = nlp(rawtext)

        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)

        results = [ent.text for ent in doc.ents if ent.label_ in labels]

        print(results)

        num_of_results = len(results)

    return render_template('index.html', results=results, num_of_results=num_of_results)
