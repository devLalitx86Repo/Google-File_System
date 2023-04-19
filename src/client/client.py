import sys
import time
import json
import requests

import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_request import post_dict
from utils.gen import make_url

MASTER_URL = ""

class File:
    def __init__(self, file_name) -> None:
        self.chunks = dict()
        self.file_name = file_name
        self.size = 0
        self.last_chunk_id = 0
    
    def request_md(self, chunk_idx):
        if chunk_idx not in self.chunks or chunk.exp_time > time.time():
            # request Master: (file_name, chunk_idx) --> chunk_md
            body = {"file_name":file_name, "chunk_idx":chunk_idx}
            response = requests.get(MASTER_URL + "/query_chunk", json=body)
            if response.status_code == 200:
                chunk_md = json.load(response.json)
                chunk = Chunk(chunk_md)
                self.chunks[chunk_idx] = chunk
                self.last_chunk_id = max(self.last_chunk_id, chunk_idx)
        else : chunk = self.chunks[chunk_idx] # key error
        return chunk
    
    def read_chunk(self, chunk_idx):
        chunk = self.request_md(chunk_idx)
        return chunk.read()
    
    def append_chunk(self, data):
        chunk = self.request_md(-1) # -1 denotes last chunk
        return chunk.append(data)
    
    def create_new_chunk(self):
        body = {"file_name":file_name, "chunk_idx":self.last_chunk_id + 1}
        response = requests.post(MASTER_URL + "/query_chunk", json=body)
        if response.status == 200:
            pass
            
class Chunk:
    def __init__(self, chunk_md) -> None:
        self.size = chunk_md["size"]
        self.handle = chunk_md["handle"]
        self.chunk_servers = chunk_md["chunk_servers"] # dict
        self.primary_server = chunk_md["primary_server"]
        self.exp_time = chunk_md["exp_time"]
        # sort chunk_servers wrt client's location
    
    def read(self, byte_range):
        for chunk_server in self.chunk_servers.values():
            # request chunk_server: (chunk_handle, byte_range) --> (status, data, check_sum)
            # parameters = {"chunk_handle":self.handle,"byte_range":byte_range}
            body = {
                "chunkHandle" : self.handle,
                "byteOffset " : byte_range[0],
                "totalBytes" : byte_range[1],
            }

            chunk_server_url = make_url(chunk_server["ip"],chunk_server["port"])
            response = requests.post(chunk_server_url, json=body)
            if response.status_code == 200:
                return json.load(response.json)
            else:
                print("Response ", response.json)
        return None
    
    def append(self, data):
        # request primary: (chunk_handle, data) --> (status)
        # parameters = {"chunk_handle":self.handle,"data":data}
        body = {
            "clientIP" : "localhost",
            "clientPort" : 6969,
            "chunkHandle" : self.handle,
            "data" : data,
            "chunkServerInfo" : self.chunk_servers
        }

        chunk_server_url = make_url(self.chunk_servers[self.primary_server]["ip"],self.chunk_servers[self.primary_server]["port"])
        response = requests.post(chunk_server_url, json=body)
        if response.status_code == 200:
            return json.load(response.json)
        else:
            print("Response ", response.json)

    def write(self, data, byteStart, byteEnd):
        body = {
            "clientIP" : "localhost",
            "clientPort" : 6969,
            "chunkHandle" : self.handle,
            "byteStart" : byteStart,
            "byteEnd" : byteEnd,
            "data" : data,
            "chunkServerInfo" : self.chunk_servers
        }

        chunk_server_url = make_url(self.chunk_servers[self.primary_server]["ip"],self.chunk_servers[self.primary_server]["port"])
        post_dict(chunk_server_url, body)

def read_handler(file_name, chunk_idx):
    if file_name not in files:
        new_file = File(file_name)
        files[file_name] = new_file

    response = files[file_name].read_chunk(chunk_idx)
    
    if response.status == 200:
        print(response)
    else:
        print("Error reading chunk:", response)

def append_handler(file_name, file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    if file_name not in files:
        new_file = File(file_name)
        files[file_name] = new_file

    for attepmts in range(3):
        response = files[file_name].append_chunk(file_data)
        if response.status_code == 200:
            print(response)
            return
        else:
            print("Error appending data:", response)
            files[file_name].create_new_chunk()
            print("waiting for 5 seconds...")
            time.sleep(5)

    print("Cannot append, try again later.")

def write_handler(file_name, file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    if file_name not in files:
        new_file = File(file_name)
        files[file_name] = new_file

    for attepmts in range(3):
        response = files[file_name].write_chunk(file_data)
        if response.status_code == 200:
            print(response)
            return
        else:
            print("Error writing data:", response)
            # print("waiting for 5 seconds...")
            # time.sleep(5)

    print("Cannot write, try again later.")

if __name__ == "__main__":
    files = dict()

    while True:
        cmd = input().split()
        try:
            if cmd[0] == "read": # read file_name chunk_idx
                file_name = cmd[1]
                chunk_idx = cmd[2]
                read_handler(file_name, chunk_idx)

            elif cmd[0] == "write": # write file_name chunk_idx local_file_path
                pass

            elif cmd[0] == "append": # append file_name local_file_path
                file_name = cmd[1]
                file_path = cmd[2]
                append_handler(file_name, file_path)

            elif cmd[0] == "create":
                pass
            
            elif cmd[0] == "delete":
                pass
            
            elif cmd[0] == "setmaster": # setmaster master_url; eg 10.37.155.40:8080
                MASTER_URL = cmd[1]

            elif cmd[0] == "exit":
                break

        except Exception as e:
            print("Invalid command")    


# if __name__ == "__main__":
#     files = dict()

#     if sys.argv[1] == "read":
#         file_name = sys.argv[2]
#         chunk_idx = sys.argv[3] 
#         read_handler(file_name, chunk_idx)
    
#     elif sys.argv[1] == "write":
#         pass
    
#     elif sys.argv[1] == "append":
#         file_name = sys.argv[2]
#         file_path = sys.argv[3] 
#         append_handler(file_name, file_path)
    
#     elif sys.argv[1] == "create":
#         pass

#     elif sys.argv[1] == "delete":
#         pass

    