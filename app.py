from flask import Flask, jsonify, request
from db_init import collection

app = Flask(__name__)

@app.route("/song", methods=["GET"])
def get_songs():
    songs = collection.find({})
    return jsonify([song for song in songs])

@app.route("/song", methods=["POST"])
def create_song():
    song = request.get_json()
    collection.insert_one(song)
    return jsonify(song), 201

@app.route("/song/<id>", methods=["GET"])
def get_song(id):
    song = collection.find_one({"_id": id})
    return jsonify(song)

@app.route("/song/<id>", methods=["PUT"])
def update_song(id):
    song = request.get_json()
    collection.update_one({"_id": id}, {"$set": song})
    return jsonify(song)

@app.route("/song/<id>", methods=["DELETE"])
def delete_song(id):
    collection.delete_one({"_id": id})
    return "", 204

@app.route("/health", methods=["GET"])
def health():
    return {"status":"OK"}, 200

@app.route("/count", methods=["GET"])
def count():
    return jsonify({"count": collection.count_documents({})})