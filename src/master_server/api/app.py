from flask import Flask, Response, jsonify, request
# from pymongo import MongoClient
import time
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

@app.route("/query_chunk", methods=["POST"])
def query_chunk_action():
    payload = request.get_json()
    filename = payload.get("file_name")
    chunk_index = payload.get("chunk_idx")
    
    #  TODO Send the time if +ve time remaining else get a new primary and send it: 
    if master_server.chunk_avail(filename,chunk_index):
        try:
            chunk = master_server.getChunk(filename,int(chunk_index))
            primary_server, avail_time = master_server.getPrimaryServer(chunk.handle)
            chunkInfo = chunk.__dict__()
            chunkInfo["expiryTime"] = avail_time
            chunkInfo["primary_server"] = primary_server
            return jsonify({"chunk_handle": chunkInfo}), 200  
        except Exception as e:
            return jsonify({"error": str(e)}), 400        
    else:
        try:
            checksum = payload.get("checksum")
            status = master_server.addChunk(filename,chunk_index,checksum)
            if status[0]:
                return json.dumps(status[1]), 200
            else:
                return jsonify({"error": status[1]}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@app.route("/initiate", methods=["POST"])
def initiate_chunk_server():
    payload = request.get_json()    
    status = master_server.addChunkServer(payload)
    if status[0]:
        return jsonify({"message": "OK"}), 200
    else:
        return jsonify({"error": status[1]}), 400

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