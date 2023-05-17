from flask import Flask, render_template, request
#from classifier import SentimentClassifier
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)



@app.route("/")
def index():
    return render_template('index.html')


@app.route("/process", methods=['POST'])
def process():
    results = []
    result = ''

    if request.method == 'POST':
        rawtext = request.form.get('rawtext')
        langoption = request.form.get('langoption')

        if langoption == 'es':
            result = 0.8
            # Manu, si has llegado hasta aquí, la librería classifier no la he encontrado y con pip3 install no va
            # El video es de hace 3 años, no se ni si está aún viva. La he buscado en google y no la encuentro

            #clf = SentimentClassifier()
            #result = clf.predict(rawtext)
        else:
            sid = SentimentIntensityAnalyzer()
            results = sid.polarity_scores(rawtext)

        print(results)

    return render_template('index.html', results=results, result=result)
