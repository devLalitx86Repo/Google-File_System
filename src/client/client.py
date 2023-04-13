import sys
import time
import json
import requests

MASTER_URL = ""

class File:
    def __init__(self, file_name) -> None:
        self.chunks = dict()
        self.file_name = file_name
        self.size = 0
    
    def request_md(self, chunk_idx):
        chunk = self.chunks[chunk_idx] # key error
        if chunk.exp_time > time.time():
            # request Master: (file_name, chunk_idx) --> chunk_md
            body = {"file_name":file_name, "chunk_idx":chunk_idx}
            response = requests.get(MASTER_URL + "/query_chunk", json=body)
            chunk_md = json.load(response.json)
            chunk = Chunk(chunk_md)
            self.chunks[chunk_idx] = chunk
        return chunk
    
    def read_chunk(self, chunk_idx):
        chunk = self.request_md(chunk_idx)
        return chunk.read()
    
    def append_chunk(self, data):
        chunk = self.request_md(-1) # -1 denotes last chunk
        return chunk.append()
    
    def create_new_chunk(self):
        body = {"file_name":file_name}
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
                "clientIP" : "localhost",
                "clientPort" : 6969,
                "chunkHandle" : self.handle,
                "byteStart" : byte_range[0],
                "byteEnd" : byte_range[1],
                "data" : "hain?",
                "chunkServerInfo" : self.chunk_servers
            }

            response = requests.post(chunk_server.id, json=body)
            return json.load(response)
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

        response = requests.post(self.chunk_servers[self.primary_server].id, json=body)
        return json.load(response)

def read_handler(file_name, chunk_idx):
    if file_name not in files:
        new_file = File(file_name)
        files[file_name] = new_file

    response = files[file_name].read_chunk(chunk_idx)
    
    if response.status == 200:
        print(response.data)
    else:
        print("Error reading chunk:", response.error)

def append_handler(file_name, file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    if file_name not in files:
        new_file = File(file_name)
        files[file_name] = new_file

    for attepmts in range(3):
        response = files[file_name].append(file_data)
        if response.status == 200:
            print(response.data)
            return
        else:
            print("Error appending data:", response.error)
            files[file_name].create_new_chunk()
            print("waiting for 3 seconds...")
            time.sleep(5)

    print("Cannot append, try again later.")

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

        except Exception as e:
            print("Invalid command")    
            