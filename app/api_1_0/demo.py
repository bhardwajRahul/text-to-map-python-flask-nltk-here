
import nltk
import requests
import tempfile
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag

from flask import jsonify
from flask.globals import request
from flask import current_app as app

from . import api


session = requests.Session()

@api.route('/geocoder', methods=['GET'])
def handle_geocoder():
    app_id = app.config['HERE_APP_ID']
    app_code = app.config['HERE_APP_CODE']
    uri = 'https://geocoder.cit.api.here.com/6.2/geocode.json'
    headers = {}
    params = {
            'app_id': app_id,
            'app_code': app_code,
            'searchtext': request.args.get('searchtext')
            }

    response = session.get(uri, headers=headers, params=params)
    return jsonify(response.json())

@api.route('/mapview', methods=['GET'])
def handle_mapview():
    app_id = app.config['HERE_APP_ID']
    app_code = app.config['HERE_APP_CODE']
    uri = 'https://image.maps.cit.api.here.com/mia/1.6/mapview'
    headers = {}
    params = {
            'app_id': app_id,
            'app_code': app_code,
            'c': request.args.get('c')
            }

    response = session.get(uri, headers=headers, params=params, stream=True)

    if request.args.get('raw'):
        return response.content
    else:
        image_path = tempfile.mktemp()
        print image_path
        open(image_path, 'wb').write(response.content)

        return image_path

@api.route('/tokenize', methods=['GET'])
def handle_tokenize():
    url = request.args.get('url')
    response = session.get(url)

    # Parse html
    body = BeautifulSoup(response.content, 'html.parser')

    # Get rid of javascript and css
    for script in body(['script', 'style']):
        script.decompose()

    text = body.get_text()

    # Ignore punctuation
    tokenizer = RegexpTokenizer(r'\w+')

    # Ignore duplicates
    tokens = set(tokenizer.tokenize(text))

    # Remove stop words
    stop_words_set = set(stopwords.words())
    tokens = [w for w in tokens if not w in stop_words_set]

    # Only interested in proper nouns
    tagged = pos_tag(tokens)
    tokens = [w for w,pos in tagged if pos in ['NNP', 'NNPS']]

    return jsonify(list(tokens))

