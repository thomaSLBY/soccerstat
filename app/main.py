from flask import Flask, render_template, jsonify
from bson.json_util import dumps
import json
import os
from mongo.main import soccerstat_db


appli = Flask(__name__)

# Takes the data from the Mongo Database. Prepares the data for Javascript.
def prepare_data(data):
    comps = []
    seasons = []
    matchweeks = []
    games = []
    i=0
    for comp,info in data.items():
        comps.append(comp)
        seasons.append([])
        matchweeks.append([])
        games.append([])
        j=0
        for season in info[0]['seasons']:
            seasons[i].append(season['name'])
            matchweeks[i].append([])
            games[i].append([])
            k = 0
            for week in season['matchweeks']:
                matchweeks[i][j].append(week['week'])
                games[i][j].append([])
                l = 0
                for game in week['games']:
                    games[i][j][k].append([])
                    games[i][j][k][l].append(game['home'])
                    games[i][j][k][l].append(game['score'])
                    games[i][j][k][l].append(game['away'])
                    games[i][j][k][l].append(game['date'])
                    games[i][j][k][l].append(game['link'])
                    l += 1
                k += 1
            j += 1
        i += 1
    
    return comps, seasons, matchweeks, games

@appli.route('/')
def home():
    comps, seasons, matchweeks, games = prepare_data(soccerstat_db.get_data())
    return render_template('index.html',
    comps = comps,
    seasons = seasons,
    matchweeks = matchweeks,
    games = games
    )

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