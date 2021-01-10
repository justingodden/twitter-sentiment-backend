# source twitter-backend/Scripts/activate

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from twitter_vader import twitter_search
# from twitter_transformer import twitter_search


app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['POST'])
def index():
    try:
        if request.is_json:
            req = request.get_json()
            json_data = twitter_search(str(req['search']))
            return json_data
    except:
        print("Something went wrong")

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
