from app import appli
from flask import Flask
from flask import render_template, jsonify
from bson.json_util import dumps
import json

if __name__=='__main__':
    appli.run(host="0.0.0.0", port=5000)