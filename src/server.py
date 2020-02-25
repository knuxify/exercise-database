#!/usr/bin/env python3
# Server for the exercise database project
# Main goals for the server:
# - Provide an API to allow clients to get information about
#   available exercises and items
# TODO:
# - Will the randomizer be a server-side function, or a client-side one?

import os
import json
import psycopg2
import argparse
import datetime

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from markupsafe import escape

# Argument parsing.
parser = argparse.ArgumentParser(description="Server for the exercise database project")
parser.add_argument("-v", "--verbose", help="Print additional information.", action="store_true")
args, unknown = parser.parse_known_args()

# Load the configuration from the config.json file.
# This file is shared across all tools.
config = json.load(open('config.json'))
# Connect to the database. No external handling is required here
# because psycopg2 breaks the program if it fails to connect.
conn = psycopg2.connect(host="localhost", database=config.get('dbname'), user=config.get('dbuser'), password=config.get('dbpass'))
cursor = conn.cursor()

# Helper functions
def log(content, verbosity):
	# Print log to output
	# Usage: log("content", verbosity [0/1])
	time = str(datetime.datetime.now().time())
	if verbosity == 0:
		print("[" + time + "] " + content)
	elif verbosity == 1 and args.verbose == True:
		print("[" + time + "] " + content)

# API
app = Flask(__name__)
api = Api(app)

class exercise(Resource):
	def get(self, exercise_id):
		query = cursor.execute("SELECT json_agg(exercises) FROM exercises WHERE exercise_id = " + exercise_id + ";")
		return cursor.fetchall()

class exercises(Resource):
	def get(self):
		query = cursor.execute("SELECT json_agg(exercises) FROM exercises;")
		return cursor.fetchall()

class item(Resource):
	def get(self, item_id):
		query = cursor.execute("SELECT json_agg(items) FROM items WHERE item_id = " + item_id + ";")
		return cursor.fetchall()

class items(Resource):
	def get(self):
		query = cursor.execute("SELECT json_agg(items) FROM items;")
		return cursor.fetchall()


api.add_resource(exercises, '/api/v1/exercises/')
api.add_resource(exercise, '/api/v1/exercises/<string:exercise_id>')
api.add_resource(items, '/api/v1/items/')
api.add_resource(item, '/api/v1/items/<string:item_id>')

if __name__ == '__main__':
    app.run(debug=True)

log("Server started!", 0)
