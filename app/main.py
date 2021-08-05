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
    return render_template('index_2.html')

@appli.route('/databases/')
def databases():
    try:
        return jsonify(soccerstat_db.get_databases())
    except Exception as e:
        return dumps({'error': str(e)})

@appli.route('/collections_mongo/')
def collections_mongo():
    return dumps(soccerstat_db.get_collection_names())

@appli.route('/competitions_mongo/')
def competitions_mongo():
    try:
        return jsonify(soccerstat_db.get_competitions())
    except Exception as e:
        return dumps({'error': str(e)})

@appli.route('/seasons_mongo/')
def seasons_mongo():
    try:
        return jsonify(soccerstat_db.get_seasons())
    except Exception as e:
        return dumps({'error': str(e)})

@appli.route('/matchweeks_mongo/')
def matchweeks_mongo():
    return jsonify(soccerstat_db.get_matchweeks())

@appli.route('/everything_mongo/')
def everything_mongo():
        return dumps(soccerstat_db.get_data())


if __name__=='__main__':
    appli.run(host="0.0.0.0", port=5000)