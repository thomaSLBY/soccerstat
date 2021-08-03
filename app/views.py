from app import appli
#from mongo import scraping_db, soccerstat_db
from flask import render_template, jsonify
from bson.json_util import dumps
import json

@appli.route('/')
def home():
    return 'coucou'