from . import app
import os
import json
import pymongo
from flask import Flask, jsonify, Blueprint, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys
from db_init import collection


app = Flask(__name__)
collection = get_collection()

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
data: list = json.load(open(json_url))

client = MongoClient(os.environ['MONGODB_SERVICE'],
                        username=os.environ['MONGODB_USERNAME'],
                        password=os.environ['MONGODB_PASSWORD'])
db = client['songs']
collection = db['songs']
#client = MongoClient('mongodb://%s:%s@127.0.0.1' % ('root', 'MzIyOTctZG9taW5p'))
#client = MongoClient(
#    f"mongodb://{app.config['MONGO_USERNAME']}:{app.config['MONGO_PASSWORD']}@localhost")
mongodb_service = os.environ.get('MONGODB_SERVICE')
mongodb_username = os.environ.get('MONGODB_USERNAME')
mongodb_password = os.environ.get('MONGODB_PASSWORD')
mongodb_port = os.environ.get('MONGODB_PORT')

print(f'The value of MONGODB_SERVICE is: {mongodb_service}')

if mongodb_service == None:
    app.logger.error('Missing MongoDB server in the MONGODB_SERVICE variable')
    # abort(500, 'Missing MongoDB server in the MONGODB_SERVICE variable')
    sys.exit(1)

if mongodb_username and mongodb_password:
    url = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_service}"
else:
    url = f"mongodb://{mongodb_service}"


print(f"connecting to url: {url}")

try:
    client = MongoClient(url)
except OperationFailure as e:
    app.logger.error(f"Authentication error: {str(e)}")

api = Blueprint('api', __name__, url_prefix='/api')
db = client.songs
db.songs.drop()
db.songs.insert_many(data)

def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"})

######################################################################
# COUNT THE NUMBER OF SONGS
######################################################################
@app.route("/count", methods=["GET"])
def count():
    """return length of data"""
    count = songs.count_documents({})
    return jsonify({"count": count}), 200

######################################################################
# COUNT THE NUMBER OF SONGS
######################################################################
@app.route("/song", methods=["GET"])
def get_songs():
    songs = list(db.songs.find({}))  # Retrieve all documents from the 'songs' collection
    formatted_songs = [{"_id": str(song['_id']), "title": song['title'], "lyrics": song['lyrics']} for song in songs]
    return jsonify({"songs": formatted_songs}), 200

if __name__ == "__main__":
    app.run()