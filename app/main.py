from flask import Flask, render_template, jsonify
from bson.json_util import dumps
import json
import os
from mongo.main import soccerstat_db

appli = Flask(__name__)

def tree_printer(root):
    for root, dirs, files in os.walk(root):
        for d in dirs:
            print(os.path.join(root, d))
        for f in files:
            print(os.path.join(root, f))

@appli.route('/')
def home():
    return jsonify(soccerstat_db.get_databases())

if __name__=='__main__':
    appli.run(host="0.0.0.0", port=5000)