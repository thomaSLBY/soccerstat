from app import appli
from flask import render_template, jsonify
from bson.json_util import dumps
import json

import sys
sys.path.append("/.../scraping/db")
from scraping import scraping_db

@appli.route('/')
def home():
    return jsonify(scraping_db.get_competitions())