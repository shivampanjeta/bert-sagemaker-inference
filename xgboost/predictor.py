# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import os
import json
#import pickle
from io import StringIO
import sys
#import signal
#import traceback

#import flask

#import pandas as pd
import xgboost

from flask import Flask
from flask import request, jsonify, abort, make_response
from flask_cors import CORS
import nltk
nltk.download('punkt')
from nltk import tokenize
from typing import List
#import argparse
from summarizer import Summarizer, TransformerSummarizer

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return flask.Response(response='\n', status=200, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
ratio = float(request.args.get('ratio', 0.2))
    summarizer = Summarizer(
            model='bert-base-uncased',
            hidden=-2,
            reduce_option='mean'
        )
    min_length = int(request.args.get('min_length', 25))
    max_length = int(request.args.get('max_length', 500))

    data = request.data
    if not data:
        abort(make_response(jsonify(message="Request must have raw text"), 400))

    parsed = Parser(data).convert_to_paragraphs()
    summary = summarizer(parsed, ratio=ratio, min_length=min_length, max_length=max_length)

    return jsonify({
        'summary': summary
    })
