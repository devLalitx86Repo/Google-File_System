from flask import Flask, Response, jsonify, request
# from pymongo import MongoClient
import json
import uuid

#Local imports
from .errors import errors, Crash_Routine
from models.Master import MasterServer
from models.Chunk import Chunk
from models.Chunk_Server import Chunk_Server
from utils.gen import generate_uuid
from utils.log import logFun

app = Flask(__name__)
app.register_blueprint(errors)

master_server = MasterServer()
Crash_Routine(master_server)

@app.route("/")
def index():
    logFun("Hello, Welcome to GFS Application!")
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
    filename = payload.get("file_name")
    chunk_index = payload.get("chunk_idx")
        
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

@app.route("/initiate", methods=["POST"])
def initiate_chunk_server():
    payload = request.get_json()
    id = payload.get("chunkServerId")
    ip = payload.get("ipAdress")
    port = payload.get("port")
    loc = payload.get("chunkLocationId")
    diskAvail = payload.get("diskAvail")
    chunk_server = Chunk_Server(ip,port,id, diskAvail, loc)
    master_server.addChunkServer(chunk_server)
    return jsonify({"message": "Chunk Server registered with Master Server"}), 200

@app.route("/get_chunk_servers", methods=["GET"])
def get_chunk_servers():
    return jsonify({"chunk_servers": master_server.getCSList()}), 200

@app.route("/ping", methods=["POST"])
def ping():
    payload = request.get_json()    
    id = payload.get("chunkServerId")
    timestamp = payload.get("timestamp")
    diskAvail = payload.get("diskAvail")
    chunkInfo_lis = payload.get("chunkInfo")
    try:
        master_server.update_ts(id,timestamp)
        master_server.update_diskAvail(id,diskAvail)
        status = master_server.update_chunkInfo(id,chunkInfo_lis)
        if status == "ERROR":
            return jsonify({"Error": "Bad Request ChunkInfo Mismatched"}), 400
        return jsonify({"message": "OK"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

    
@app.route("/ack", methods=["POST"])
def ack():
    pass