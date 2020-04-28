# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.
import json
import xgboost
import flask
from flask import Flask
from flask import request, jsonify, abort, make_response
from gensim.summarization.summarizer import summarize

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return flask.Response(response='\n', status=200, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    data = request.data
    summary = summarize(data)
    return jsonify({
        'summary': summary
    })
