from flask import Flask, Response, jsonify, request
# from pymongo import MongoClient
import json
import uuid


#Local imports
from .errors import errors
from models.Master import MasterServer
from models.Chunk import Chunk
from .utils.gen import generate_uuid

app = Flask(__name__)
app.register_blueprint(errors)

master_server = MasterServer()

@app.route("/")
def index():
    return Response("Hello, Welcome to GFS Application!", status=200)


@app.route("/custom", methods=["POST"])
def custom():
    payload = request.get_json()

    if payload.get("say_hello") is True:
        output = jsonify({"message": "Hello!"})
    else:
        output = jsonify({"message": "..."})

    return output

@app.route("/get_random_id", methods=["GET"])
def get_random_id():
    id = uuid.uuid1().int>>64
    return jsonify({"id": str(id)})

@app.route("/query_chunk", methods=["GET","POST","UPDATE"])
def query_chunk_action():
    payload = request.get_json()
    filename = payload.get("filename")
    chunk_index = payload.get("index")
        
    if request.method == "GET":
        try:
            chunk = master_server.getChunk(filename,chunk_index)
            return jsonify({"chunk_handle": chunk.__dict__()}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    elif request.method == "POST":
        try:
            chunk_checksum = payload.get("checksum")
            chunk_handle = generate_uuid()
            chunk = Chunk(filename,chunk_checksum,chunk_index,chunk_handle)
            master_server.addChunk(chunk)
            return jsonify({"chunk_handle": chunk_handle}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

