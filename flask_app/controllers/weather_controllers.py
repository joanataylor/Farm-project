from flask_app import app
import datetime as dt
import requests
from flask_cors import CORS
from flask import render_template, jsonify
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# @app.route('/api')
# def api():

#     my_data = {
#       "usesAJAX" : "true",
#       "2plus2" : 4
#     }

#     return jsonify(my_data)